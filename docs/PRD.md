# Product Requirements Document — IS590 AI Agent

## Problem Statement
Students and practitioners working with AI concepts need a hands-on demonstration of how modern AI agents work. Reading about LLMs, RAG, and tool use is abstract; interacting with a working agent that shows its reasoning and tool calls in real time makes these concepts concrete. Additionally, a general-purpose assistant that can do math, look up current information, and answer questions from a curated knowledge base covers a wide range of real-world use cases in a single coherent interface.

## Product Goal
Build a multi-tool AI agent with a web chat interface that demonstrates the ReAct (Reasoning + Acting) pattern using LangChain. The agent must feel responsive (streaming), be conversationally coherent (memory), and transparently show when it is using tools.

---

## Users
**Primary**: IS590 course instructor and graders evaluating the assignment.
**Secondary**: The student (developer) demonstrating the agent in the 2-minute video walkthrough.

---

## Tools

### 1. Calculator
**What it does**: Evaluates mathematical expressions safely.
**Why**: LLMs are notoriously unreliable at arithmetic. Delegating math to a deterministic tool produces correct answers every time.
**Implementation**: AST-based evaluator — no `eval()`, only whitelisted operators and `math` functions. Supports: `+`, `-`, `*`, `/`, `**`, `%`, `//`, `sqrt`, `sin`, `cos`, `tan`, `log`, `log10`, `abs`, `ceil`, `floor`, `exp`, `factorial`, constants `pi` and `e`.
**Trigger examples**: "What is 15% of 847?", "sqrt(2) * pi", "factorial(10)"

### 2. Web Search
**What it does**: Retrieves current information from the web via the Tavily search API.
**Why**: LLMs have a knowledge cutoff and cannot answer questions about recent events or live data without retrieval.
**Implementation**: Tavily client, `max_results=5`, returns title + content + source URL for each result.
**Trigger examples**: "What happened in AI news this week?", "Current price of NVIDIA stock", "Who won the Super Bowl?"

### 3. RAG (Retrieval-Augmented Generation)
**What it does**: Searches a curated knowledge base of local documents using vector similarity and returns sourced excerpts.
**Why**: Demonstrates private/domain-specific knowledge retrieval — a core enterprise use case for LLMs. Provides source attribution so users can verify answers.
**Implementation**: ChromaDB (ephemeral) + OpenAI embeddings. Documents in `docs/` are chunked (~300 words, 50-word overlap) and indexed at startup. Top-3 chunks returned with `[Source: filename]` attribution.
**Knowledge base documents** (6 total):
  - `ai_concepts.md` — LLMs, RAG, embeddings, vector DBs, agents, CoT, tokens, temperature
  - `python_reference.md` — Python syntax, async, typing, common libraries
  - `langchain_reference.md` — LangChain tools, agents, LCEL, memory, streaming
  - `fastapi_reference.md` — FastAPI routes, Pydantic, SSE, static files, startup events
  - `machine_learning_fundamentals.md` — supervised/unsupervised learning, neural nets, training
  - `prompt_engineering.md` — zero/few-shot, CoT, ReAct, structured output, pitfalls
**Trigger examples**: "What is the ReAct pattern?", "How does RAG work?", "Explain embeddings"

---

## Conversation Memory
The agent maintains per-session conversation history (up to 20 messages). Follow-up questions like "what about its limitations?" work correctly because the full prior context is included in every LLM call. Sessions are identified by a UUID stored in `localStorage`.

---

## Web UI
- Single-page chat interface at `http://localhost:8000`
- Real-time streaming via SSE — tokens appear as they are generated
- Tool badges appear inline in the conversation when tools are invoked
- Sample prompt chips on the welcome screen
- Clear chat button resets the session
- Keyboard shortcut: Enter to send, Shift+Enter for newline

---

## Non-Functional Requirements
| Requirement | Target |
|---|---|
| Streaming latency | First token within 2s of sending message |
| Tool transparency | Tool name visible in UI during invocation |
| Source attribution | RAG responses always include `[Source: filename]` |
| Safety | Calculator uses AST only; no arbitrary code execution |
| Logging | All tool calls logged with args and results (JSON to stdout) |
| Memory limit | Max 20 messages per session to control token cost |

---

## Out of Scope
- User authentication
- Persistent vector store (ephemeral Chroma is sufficient for the demo)
- Multi-user production deployment
- Fine-tuning the LLM
- Voice input/output
