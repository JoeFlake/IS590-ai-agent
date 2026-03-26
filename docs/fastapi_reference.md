# FastAPI Reference — Building the Surf Shack Backend

Bro, FastAPI is the pipeline of the surf world. It gets your requests from the beach to the wave and back faster than anyone else. Async, typed, automatic docs — it's the perfect backend for an AI agent surf shack.

## What is FastAPI?

FastAPI is a modern Python web framework for building APIs. Key features:
- **Async-first** — built on ASGI/Starlette, handles concurrent requests without blocking
- **Type hints** — uses Pydantic for automatic request validation
- **Auto docs** — generates OpenAPI/Swagger UI at `/docs` automatically
- **High performance** — comparable to Node.js and Go

## Basic App Setup

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Chicken Joe's Surf Shack API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
```

CORS middleware lets your browser frontend talk to the backend without getting wiped out by browser security.

## Request Models with Pydantic

```python
from pydantic import BaseModel

class ChatRequest(BaseModel):
    message: str
    session_id: str = "default"  # optional with default
```

FastAPI automatically validates incoming JSON against this model. Wrong types = 422 error before your code even runs. Clean, dude.

## Route Handlers

```python
@app.get("/health")
async def health():
    return {"status": "ok", "vibe": "totally tubular"}

@app.post("/chat")
async def chat(request: ChatRequest):
    # request.message and request.session_id are validated and typed
    return {"response": "Hang loose!"}
```

Always use `async def` for route handlers in FastAPI — it lets the server handle other requests while yours is waiting on an LLM or database.

## Server-Sent Events (SSE) for Streaming

SSE is how Chicken Joe's Surf Shack streams tokens in real time. The server pushes data chunks as they arrive instead of waiting for the full response:

```python
from fastapi.responses import StreamingResponse
import json

@app.post("/chat")
async def chat(request: ChatRequest):
    async def generate():
        async for token in llm.astream(request.message):
            data = json.dumps({"type": "content", "content": token})
            yield f"data: {data}\n\n"  # SSE format: "data: ...\n\n"
        yield f"data: {json.dumps({'type': 'done'})}\n\n"

    return StreamingResponse(
        generate(),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )
```

The `X-Accel-Buffering: no` header tells proxies (like Nginx) not to buffer the stream — critical for real-time delivery.

## Startup Events

Run code when the server starts (like preloading the RAG vectorstore):

```python
@app.on_event("startup")
async def startup():
    get_vectorstore()  # build and cache the Chroma index
```

This runs once before any requests are handled. Great for expensive initialization.

## Serving Static Files

To serve a frontend from a `static/` folder:

```python
from fastapi.staticfiles import StaticFiles

app.mount("/", StaticFiles(directory="static", html=True), name="static")
```

`html=True` means `index.html` is served for bare `/` requests. Mount this LAST, after all your API routes, or it'll swallow your endpoints.

## Running with Uvicorn

```bash
uvicorn app.main:app --reload
```

- `app.main:app` — module path `app/main.py`, variable `app`
- `--reload` — auto-restart on file changes (development mode only)
- Default: `http://127.0.0.1:8000`

For production you'd use `--workers 4` and skip `--reload`.

## Path Structure

```
app/
├── main.py        # FastAPI app, routes, startup
├── agent.py       # LangChain agent
├── logger.py      # Structured JSON logging
└── tools/
    ├── calculator.py
    ├── web_search.py
    └── rag.py
static/
├── index.html
├── style.css
└── app.js
```

FastAPI's `StaticFiles` mount serves everything in `static/` directly. The agent tools are imported into `main.py` and wired into the LangChain agent.

## Error Handling

```python
from fastapi import HTTPException

@app.get("/wipeout")
async def wipeout():
    raise HTTPException(status_code=404, detail="Wave not found, dude")
```

FastAPI converts exceptions into proper JSON error responses automatically.

## Auto-Generated Docs

When your server is running, visit:
- `http://localhost:8000/docs` — Swagger UI (interactive)
- `http://localhost:8000/redoc` — ReDoc (clean reference)

Totally radical for testing your endpoints without writing a frontend first.
