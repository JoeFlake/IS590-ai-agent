# IS590 AI Agent

A multi-tool AI agent with a streaming web chat interface, built for IS590 (AI Applications). Demonstrates the ReAct (Reasoning + Acting) pattern using LangChain, FastAPI, and ChromaDB.

## Features

| Feature | Details |
|---|---|
| **Calculator** | Safe AST-based math evaluator — no `eval()`. Supports arithmetic, trig, log, factorial, `pi`, `e`. |
| **Web Search** | Live web search via Tavily API. Returns titles, summaries, and source URLs. |
| **RAG** | Vector search over 6 local knowledge base documents using ChromaDB + OpenAI embeddings. Every result includes `[Source: filename]` attribution. |
| **Memory** | Per-session conversation history (up to 20 messages). Follow-up questions work correctly. |
| **Streaming** | Real-time token streaming via Server-Sent Events (SSE). Tool invocations shown inline as badges. |
| **Structured Logging** | JSON logs to stdout for every tool call, including tool name, arguments, and result preview. |

## Setup

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure environment variables
```bash
cp .env.example .env
```

Edit `.env` and fill in your API keys:

| Variable | Where to Get It |
|---|---|
| `OPENAI_API_KEY` | [platform.openai.com/api-keys](https://platform.openai.com/api-keys) |
| `TAVILY_API_KEY` | [tavily.com](https://tavily.com) — free tier available |

### 3. Run the server
```bash
uvicorn app.main:app --reload
```

Open [http://localhost:8000](http://localhost:8000) in your browser.

## Project Structure

```
├── app/
│   ├── main.py           # FastAPI app — SSE /chat, /clear, /health endpoints
│   ├── agent.py          # LangChain agent (tools, prompt, AgentExecutor)
│   ├── logger.py         # Structured JSON logger (used by all tools + server)
│   └── tools/
│       ├── calculator.py # Safe AST-based math evaluator
│       ├── web_search.py # Tavily web search
│       └── rag.py        # ChromaDB vector search with source attribution
├── docs/                 # RAG knowledge base (Markdown files)
│   ├── ai_concepts.md
│   ├── python_reference.md
│   ├── langchain_reference.md
│   ├── fastapi_reference.md
│   ├── machine_learning_fundamentals.md
│   ├── prompt_engineering.md
│   ├── PRD.md            # Product Requirements Document
│   └── ROADMAP.md        # Phased roadmap with progress tracking
├── static/
│   ├── index.html        # Chat UI
│   ├── style.css         # Styles
│   └── app.js            # SSE client, session management
├── context.md            # Project orientation for AI coding tools
├── .env.example          # Environment variable template
└── requirements.txt      # Python dependencies
```

## How It Works

1. User sends a message in the chat UI
2. The frontend POSTs to `/chat` and opens an SSE stream
3. The LangChain `AgentExecutor` decides which tool(s) to call (ReAct pattern)
4. Tool calls are logged (JSON to stdout) and streamed as badge events to the UI
5. The LLM's response tokens stream back in real time
6. The full exchange is appended to the session's conversation history

## Adding to the Knowledge Base

Drop any `.md` or `.txt` file into `docs/` and restart the server. The RAG tool automatically discovers and indexes all documents in that directory at startup.

## Example Prompts

- `What is 15% of 847 plus the square root of 2?` — uses Calculator
- `What are the latest AI news headlines?` — uses Web Search  
- `How does the ReAct pattern work?` — uses RAG
- `Explain embeddings, then find a recent paper about them` — uses RAG then Web Search

## Logging

Every tool invocation emits a structured JSON log line to stdout:

```json
{"ts": "2026-03-23T20:00:00Z", "level": "INFO", "logger": "tool.calculator",
 "message": "tool_call", "tool": "calculator",
 "args": {"expression": "sqrt(144) + 2**8"}, "result_preview": "268.0"}
```

Fields logged: `tool`, `args`, `result_preview`, `result_length` (or `error` on failure).
