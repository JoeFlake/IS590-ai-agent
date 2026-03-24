import json
import os
from typing import Dict, List

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from fastapi.staticfiles import StaticFiles
from langchain_core.messages import AIMessage, HumanMessage
from pydantic import BaseModel

load_dotenv()

from app.agent import create_agent
from app.logger import get_logger
from app.tools.rag import get_vectorstore

_log = get_logger("agent.server")

app = FastAPI(title="IS590 AI Agent")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

agent_executor = create_agent()
conversations: Dict[str, List] = {}


class ChatRequest(BaseModel):
    message: str
    session_id: str = "default"


class ClearRequest(BaseModel):
    session_id: str = "default"


@app.on_event("startup")
async def startup():
    _log.info("startup", extra={"event": "server_start", "action": "preloading RAG vectorstore"})
    get_vectorstore()
    _log.info("startup", extra={"event": "server_ready"})


@app.post("/chat")
async def chat(request: ChatRequest):
    history = conversations.get(request.session_id, [])
    _log.info(
        "chat_request",
        extra={
            "session_id": request.session_id,
            "message_preview": request.message[:100],
            "history_length": len(history),
        },
    )

    async def generate():
        collected = []
        try:
            async for event in agent_executor.astream_events(
                {"input": request.message, "chat_history": history},
                version="v2",
            ):
                etype = event["event"]
                if etype == "on_chat_model_stream":
                    chunk = event["data"]["chunk"]
                    if chunk.content:
                        collected.append(chunk.content)
                        yield f"data: {json.dumps({'type': 'content', 'content': chunk.content})}\n\n"
                elif etype == "on_tool_start":
                    tool_name = event.get("name", "")
                    tool_input = event.get("data", {}).get("input", {})
                    _log.info(
                        "tool_start",
                        extra={"session_id": request.session_id, "tool": tool_name, "input": tool_input},
                    )
                    yield f"data: {json.dumps({'type': 'tool_start', 'tool': tool_name})}\n\n"
                elif etype == "on_tool_end":
                    tool_name = event.get("name", "")
                    tool_output = str(event.get("data", {}).get("output", ""))
                    _log.info(
                        "tool_end",
                        extra={
                            "session_id": request.session_id,
                            "tool": tool_name,
                            "output_preview": tool_output[:200],
                            "output_length": len(tool_output),
                        },
                    )
                    yield f"data: {json.dumps({'type': 'tool_end', 'tool': tool_name})}\n\n"

            full_response = "".join(collected)
            history.append(HumanMessage(content=request.message))
            history.append(AIMessage(content=full_response))
            conversations[request.session_id] = history[-20:]
            _log.info(
                "chat_response",
                extra={
                    "session_id": request.session_id,
                    "response_length": len(full_response),
                    "history_length": len(conversations[request.session_id]),
                },
            )
            yield f"data: {json.dumps({'type': 'done'})}\n\n"

        except Exception as exc:
            _log.error("chat_error", extra={"session_id": request.session_id, "error": str(exc)})
            yield f"data: {json.dumps({'type': 'error', 'content': str(exc)})}\n\n"

    return StreamingResponse(
        generate(),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )


@app.post("/clear")
async def clear(request: ClearRequest):
    conversations.pop(request.session_id, None)
    _log.info("session_cleared", extra={"session_id": request.session_id})
    return {"status": "cleared"}


@app.get("/health")
async def health():
    return {"status": "ok"}


static_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "static")
app.mount("/", StaticFiles(directory=static_dir, html=True), name="static")
