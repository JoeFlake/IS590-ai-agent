# Project Context

This file orients AI coding assistants to the IS590 AI Agent project.

## What This Is
A multi-tool AI agent built for IS590 (AI Applications). It is a streaming chat web application where users interact with a LangChain-powered agent that can use three tools: a calculator, a web search engine, and a RAG knowledge base. The agent demonstrates the ReAct pattern with multi-turn conversation memory.

## Tech Stack
- **Backend**: Python 3.11+, FastAPI, Uvicorn (ASGI)
- **AI/Agent**: LangChain (`langchain`, `langchain-openai`, `langchain-chroma`)
- **LLM**: OpenAI `gpt-4o-mini` via `langchain_openai.ChatOpenAI`
- **Embeddings**: OpenAI `text-embedding-ada-002` via `OpenAIEmbeddings`
- **Vector Store**: ChromaDB (ephemeral in-memory, rebuilt on startup)
- **Web Search**: Tavily API via `tavily-python`
- **Frontend**: Vanilla HTML/CSS/JS, served as static files from FastAPI
- **Streaming**: Server-Sent Events (SSE) via `StreamingResponse`
- **Logging**: Structured JSON logging via `app/logger.py`

## Project Structure
```
aiDocs/            — AI dev infrastructure (context, PRD, roadmap)
app/
  main.py          — FastAPI app, /chat SSE endpoint, /clear, /health
  agent.py         — LangChain agent setup (tools, prompt, AgentExecutor)
  logger.py        — Structured JSON logger used by all tools and server
  tools/
    calculator.py  — Safe AST-based math evaluator (@tool)
    web_search.py  — Tavily web search (@tool)
    rag.py         — ChromaDB vector search over docs/ (@tool)
docs/              — Markdown knowledge base files ingested by RAG at startup
scripts/
  test.sh          — Smoke tests: imports, calculator, RAG doc count, health
static/
  index.html       — Chat UI
  style.css        — Styles
  app.js           — SSE client, message rendering, session management
.env.example       — Required env vars template
requirements.txt   — Python dependencies
```

## Running the Project
```bash
pip install -r requirements.txt
cp .env.example .env   # then add OPENAI_API_KEY and TAVILY_API_KEY
uvicorn app.main:app --reload
# open http://localhost:8000
```

## Environment Variables
| Variable | Where to Get It |
|---|---|
| `OPENAI_API_KEY` | https://platform.openai.com/api-keys |
| `TAVILY_API_KEY` | https://tavily.com (free tier available) |

## Key Design Decisions
- **Ephemeral ChromaDB**: The vector store is rebuilt in memory on every startup from the `docs/` folder. No persistence needed for a course project; swap to `chromadb.PersistentClient` for production.
- **Session memory in-process**: Conversation history is stored in a Python dict keyed by `session_id`. Not durable across restarts.
- **SSE not WebSockets**: SSE is simpler (one-way server push, works with plain `fetch`), sufficient for a chat stream.
- **gpt-4o-mini**: Cheaper than gpt-4o, fast enough for demos, and supports function calling needed for tool use.
- **AST calculator**: Avoids `eval()` security issues by only allowing safe math operations via Python's AST module.

## Adding New RAG Documents
Drop any `.md` or `.txt` file into `docs/` and restart the server. The RAG tool auto-discovers and indexes all files in that directory.

## Logging
All tool calls emit structured JSON logs to stdout:
- `tool.calculator` — expression + result
- `tool.web_search` — query + num results
- `tool.rag` — query + sources + num chunks
- `agent.server` — request metadata, tool start/end events, response stats
