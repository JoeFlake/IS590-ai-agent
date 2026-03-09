# IS590 AI Agent

A mini agentic application with a web chat interface, built for IS590.

## Features
- **Calculator** – evaluates math expressions safely via AST parsing
- **Web Search** – live web search via Tavily
- **RAG** – in-memory vector search over local docs (ChromaDB + OpenAI embeddings)
- **Chat UI** – clean streaming web interface
- **Conversation Memory** – multi-turn context per session

## Setup

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure environment variables
```bash
cp .env.example .env
# Edit .env and add your API keys
```

You need:
- `OPENAI_API_KEY` — from https://platform.openai.com
- `TAVILY_API_KEY` — from https://tavily.com (free tier available)

### 3. Run the server
```bash
uvicorn app.main:app --reload
```

Open http://localhost:8000 in your browser.

## Project Structure
```
├── app/
│   ├── main.py          # FastAPI app + streaming SSE endpoint
│   ├── agent.py         # LangChain agent with tools
│   └── tools/
│       ├── calculator.py  # Safe AST-based math evaluator
│       ├── web_search.py  # Tavily web search
│       └── rag.py         # In-memory ChromaDB RAG
├── static/              # Frontend (HTML/CSS/JS)
├── docs/                # Knowledge base documents for RAG
├── .env.example
└── requirements.txt
```
