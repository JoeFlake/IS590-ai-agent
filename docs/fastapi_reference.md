# FastAPI Reference

## What is FastAPI?
FastAPI is a modern, high-performance Python web framework for building APIs. It is built on Starlette (ASGI) and Pydantic, and supports async/await natively. FastAPI auto-generates OpenAPI (Swagger) docs and is one of the fastest Python frameworks available.

## Key Features
- **Async support**: Uses Python's `asyncio` and `async def` for non-blocking I/O
- **Type hints**: Request/response models defined with Pydantic, validated automatically
- **Auto docs**: Swagger UI at `/docs`, ReDoc at `/redoc`
- **Dependency injection**: Clean way to share logic (DB sessions, auth) across routes
- **ASGI**: Runs on Uvicorn or Hypercorn, enabling WebSockets, SSE, and streaming

## Basic App Structure
```python
from fastapi import FastAPI
app = FastAPI(title="My API")

@app.get("/")
async def root():
    return {"message": "Hello"}
```

## Request and Response Models
Pydantic `BaseModel` classes define the shape of request bodies and responses. FastAPI validates incoming JSON automatically and returns 422 Unprocessable Entity if validation fails.

```python
from pydantic import BaseModel

class ChatRequest(BaseModel):
    message: str
    session_id: str = "default"
```

## Path Operations
FastAPI supports standard HTTP methods via decorators: `@app.get`, `@app.post`, `@app.put`, `@app.delete`, `@app.patch`. Route parameters are declared as function arguments with type hints.

## Streaming Responses (SSE)
`StreamingResponse` enables server-sent events (SSE) and chunked transfer encoding. An async generator yields chunks as they become available. SSE uses `text/event-stream` MIME type with the format `data: <payload>\n\n`.

```python
from fastapi.responses import StreamingResponse

async def generate():
    yield "data: chunk1\n\n"
    yield "data: chunk2\n\n"

return StreamingResponse(generate(), media_type="text/event-stream")
```

## Static Files
`StaticFiles` mounts a directory to serve static assets (HTML, CSS, JS). With `html=True`, it serves `index.html` at the root URL. This allows FastAPI to host a full single-page application alongside the API.

## CORS Middleware
`CORSMiddleware` enables cross-origin requests. In development, `allow_origins=["*"]` permits all origins. In production, restrict to specific domains.

## Startup Events
`@app.on_event("startup")` runs async code when the server starts — ideal for loading models, connecting to databases, or preloading vector stores.

## Uvicorn
Uvicorn is the ASGI server that runs FastAPI. `uvicorn app.main:app --reload` starts the server with hot reload for development. `--host 0.0.0.0` binds to all interfaces. `--port 8000` sets the port.

## Error Handling
FastAPI catches `HTTPException` and returns structured JSON error responses. `try/except` inside route handlers can catch application errors and return appropriate responses or stream error events.
