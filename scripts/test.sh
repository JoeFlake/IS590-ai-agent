#!/usr/bin/env bash
# scripts/test.sh — smoke tests for IS590 AI Agent
# Tests imports, tool logic, and server health.
# Exit code 0 = all passed, 1 = one or more failures.

set -euo pipefail

PASS=0
FAIL=0
SERVER_URL="http://localhost:8000"

# ── helpers ──────────────────────────────────────────────────────────────────

ok()   { echo "[PASS] $1"; PASS=$((PASS + 1)); }
fail() { echo "[FAIL] $1"; FAIL=$((FAIL + 1)); }

# ── 1. Environment ────────────────────────────────────────────────────────────

echo ""
echo "=== Environment checks ==="

if [ -f ".env" ]; then
    ok ".env file exists"
else
    fail ".env file missing — copy .env.example and add your API keys"
fi

if grep -q "OPENAI_API_KEY" .env.example 2>/dev/null; then
    ok ".env.example has OPENAI_API_KEY"
else
    fail ".env.example missing OPENAI_API_KEY"
fi

if grep -q "TAVILY_API_KEY" .env.example 2>/dev/null; then
    ok ".env.example has TAVILY_API_KEY"
else
    fail ".env.example missing TAVILY_API_KEY"
fi

# ── 2. Python imports ─────────────────────────────────────────────────────────

echo ""
echo "=== Python import checks ==="

python3 -c "from app.tools.calculator import calculator" 2>/dev/null \
    && ok "calculator tool imports" \
    || fail "calculator tool import failed"

python3 -c "from app.tools.web_search import web_search" 2>/dev/null \
    && ok "web_search tool imports" \
    || fail "web_search tool import failed"

python3 -c "from app.logger import get_logger, log_tool_call" 2>/dev/null \
    && ok "logger module imports" \
    || fail "logger module import failed"

python3 -c "from app.agent import create_agent" 2>/dev/null \
    && ok "agent module imports" \
    || fail "agent module import failed"

# ── 3. Calculator logic (no API key needed) ───────────────────────────────────

echo ""
echo "=== Calculator tool tests ==="

RESULT=$(python3 -c "
from app.tools.calculator import calculator
print(calculator.invoke({'expression': '2 + 2'}))
" 2>/dev/null)
if [ "$RESULT" = "4" ]; then
    ok "calculator: 2 + 2 = 4"
else
    fail "calculator: expected 4, got '$RESULT'"
fi

RESULT=$(python3 -c "
from app.tools.calculator import calculator
print(calculator.invoke({'expression': 'sqrt(144)'}))
" 2>/dev/null)
if [ "$RESULT" = "12.0" ]; then
    ok "calculator: sqrt(144) = 12.0"
else
    fail "calculator: expected 12.0, got '$RESULT'"
fi

RESULT=$(python3 -c "
from app.tools.calculator import calculator
r = calculator.invoke({'expression': '__import__(\"os\")'})
print(r)
" 2>/dev/null)
if echo "$RESULT" | grep -qi "error"; then
    ok "calculator: blocks unsafe expressions"
else
    fail "calculator: did not block unsafe expression — got '$RESULT'"
fi

# ── 4. RAG document coverage ──────────────────────────────────────────────────

echo ""
echo "=== RAG knowledge base checks ==="

DOC_COUNT=$(ls docs/*.md docs/*.txt 2>/dev/null | wc -l)
if [ "$DOC_COUNT" -ge 5 ]; then
    ok "docs/ contains $DOC_COUNT documents (minimum 5 required)"
else
    fail "docs/ contains only $DOC_COUNT documents — need at least 5"
fi

# ── 5. Server health (only if already running) ────────────────────────────────

echo ""
echo "=== Server health check (skipped if not running) ==="

if curl -sf "$SERVER_URL/health" > /dev/null 2>&1; then
    STATUS=$(curl -s "$SERVER_URL/health" | python3 -c "import sys,json; print(json.load(sys.stdin).get('status',''))" 2>/dev/null)
    if [ "$STATUS" = "ok" ]; then
        ok "server /health returns {\"status\": \"ok\"}"
    else
        fail "server /health returned unexpected status: $STATUS"
    fi
else
    echo "[SKIP] server not running at $SERVER_URL — start with: uvicorn app.main:app --reload"
fi

# ── 6. Repo structure ─────────────────────────────────────────────────────────

echo ""
echo "=== Repo structure checks ==="

for f in "aiDocs/context.md" "aiDocs/PRD.md" "aiDocs/ROADMAP.md" \
          "app/logger.py" "app/agent.py" "app/main.py" \
          "app/tools/calculator.py" "app/tools/web_search.py" "app/tools/rag.py" \
          "static/index.html" ".env.example" "requirements.txt" "README.md"; do
    if [ -f "$f" ]; then
        ok "$f exists"
    else
        fail "$f MISSING"
    fi
done

# ── Summary ───────────────────────────────────────────────────────────────────

echo ""
echo "============================================"
echo "Results: $PASS passed, $FAIL failed"
echo "============================================"

if [ "$FAIL" -gt 0 ]; then
    exit 1
fi
exit 0
