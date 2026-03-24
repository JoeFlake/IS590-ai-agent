# Project Roadmap — IS590 AI Agent

## Phase 1 — Project Setup ✅
*Goal: Scaffold the repo with correct structure, dependencies, and configuration.*

- [x] Initialize git repository
- [x] Create `requirements.txt` with all dependencies
- [x] Create `.env.example` with required environment variable keys
- [x] Create `.gitignore` (exclude `.env`, `__pycache__`, `.venv`, `.chroma`, `node_modules`)
- [x] Scaffold `app/` package with `main.py`, `agent.py`, `tools/` directory
- [x] Write initial `README.md`

---

## Phase 2 — Core Tools ✅
*Goal: Implement and test all three agent tools in isolation.*

- [x] **Calculator tool** (`app/tools/calculator.py`)
  - Safe AST-based evaluator
  - Supports arithmetic, trig, log, factorial, constants pi and e
- [x] **Web Search tool** (`app/tools/web_search.py`)
  - Tavily API integration
  - Returns title, content, and source URL for top 5 results
- [x] **RAG tool** (`app/tools/rag.py`)
  - ChromaDB ephemeral vector store
  - OpenAI embeddings for indexing and retrieval
  - Word-based chunking (300 words, 50 overlap)
  - Source attribution in results (`[Source: filename]`)

---

## Phase 3 — Agent & Memory ✅
*Goal: Wire tools into a LangChain agent with conversation memory.*

- [x] Create `app/agent.py` with `create_openai_tools_agent`
- [x] Configure `ChatOpenAI` (`gpt-4o-mini`, `temperature=0`, streaming)
- [x] Build `ChatPromptTemplate` with `chat_history` placeholder for memory
- [x] Wrap in `AgentExecutor` (`handle_parsing_errors=True`, `max_iterations=5`)
- [x] Per-session memory in `main.py` (dict of message lists, capped at 20)

---

## Phase 4 — Web UI ✅
*Goal: Build a streaming chat frontend served by FastAPI.*

- [x] FastAPI app with SSE `/chat` endpoint (`app/main.py`)
- [x] `StreamingResponse` with `astream_events` v2
- [x] Static file mount serving `static/` at root
- [x] `static/index.html` — chat layout with welcome chips
- [x] `static/style.css` — responsive design, tool badges, streaming cursor
- [x] `static/app.js` — SSE client, session management via `localStorage`, tool badges
- [x] CORS middleware, `/health` endpoint, `/clear` endpoint

---

## Phase 5 — RAG Knowledge Base ✅
*Goal: Populate the knowledge base with at least 5 real documents.*

- [x] `docs/ai_concepts.md` — LLMs, RAG, embeddings, agents, CoT, tokens, temperature
- [x] `docs/python_reference.md` — Python structures, async, typing, common libraries
- [x] `docs/langchain_reference.md` — LangChain tools, agents, LCEL, memory, streaming
- [x] `docs/fastapi_reference.md` — FastAPI routes, Pydantic, SSE, static files
- [x] `docs/machine_learning_fundamentals.md` — supervised/unsupervised learning, transformers
- [x] `docs/prompt_engineering.md` — zero/few-shot, CoT, ReAct, structured output

---

## Phase 6 — Polish & Repo Hygiene ✅
*Goal: Meet all repo requirements for the assignment submission.*

- [x] **Structured logging** — JSON logger in `app/logger.py`, used in all tools and server
  - Logs: tool name, input args, result preview, result length
  - Logs: session ID, message metadata, tool start/end events
- [x] **`context.md`** — orients AI tools to the project tech stack and design decisions
- [x] **`docs/PRD.md`** — product requirements: problem, tools, memory, UI, non-functional
- [x] **`docs/ROADMAP.md`** — this file; phased plan with progress tracked
- [x] **`README.md`** — updated with full setup instructions, project structure, features
- [x] Incremental git commits (5+) showing setup → tools → agent → UI → RAG → polish

---

## Backlog (Not Required for Assignment)
*Nice-to-haves if time permits.*

- [ ] Persistent ChromaDB (survive server restarts)
- [ ] LangSmith tracing integration
- [ ] Docker / docker-compose for reproducible deployment
- [ ] Rate limiting on `/chat` endpoint
- [ ] Token usage tracking and display in UI
- [ ] Additional RAG document types (PDF ingestion)
