# LangChain Reference

## What is LangChain?
LangChain is an open-source framework for building applications powered by large language models. It provides abstractions for chaining together LLM calls, tool use, memory, and retrieval into cohesive pipelines called "chains" and "agents." LangChain supports Python and JavaScript/TypeScript.

## Core Abstractions

### LLMs and Chat Models
LangChain wraps model providers (OpenAI, Anthropic, Google, etc.) behind a uniform interface. `ChatOpenAI` is the standard wrapper for OpenAI's chat completion API. Models accept a list of messages (system, human, AI) and return an AI message.

### Prompts and Prompt Templates
`ChatPromptTemplate` composes multi-turn prompt structures. `MessagesPlaceholder` inserts a list of messages (e.g., chat history) at a named slot. This enables dynamic, history-aware prompts without string manipulation.

### Chains
Chains pipe outputs of one component into the next using the LCEL (LangChain Expression Language) `|` operator. Example: `prompt | llm | output_parser`. Chains are composable, inspectable, and streamable.

### Tools
Tools are Python functions decorated with `@tool` that the agent can call. LangChain uses the function's docstring as the tool description fed to the LLM. Tools must have typed inputs (single string or Pydantic model) and return a string result.

### Agents
Agents use an LLM to reason about which tools to call. `create_openai_tools_agent` uses OpenAI's native function-calling API for reliable tool selection. `AgentExecutor` wraps the agent in a loop that runs until the agent returns a final answer or hits `max_iterations`.

### AgentExecutor
`AgentExecutor` orchestrates the agent loop: plan → call tool → observe result → repeat. Key parameters: `handle_parsing_errors=True` (gracefully recovers from malformed outputs), `max_iterations` (prevents infinite loops), `verbose` (logs reasoning steps).

## Memory
LangChain supports several memory types. For multi-turn chat, `ConversationBufferMemory` stores the full message history. In custom implementations, you can maintain a list of `HumanMessage` / `AIMessage` objects and pass them via `chat_history` to the agent prompt.

## Streaming
LangChain supports async streaming via `astream_events`. The `v2` event schema emits typed events: `on_chat_model_stream` (partial tokens), `on_tool_start` (tool invocation begins), `on_tool_end` (tool returns result), `on_chain_end` (full completion). This enables real-time streaming UIs.

## RAG with LangChain
LangChain integrates with vector stores via `langchain-chroma`, `langchain-pinecone`, etc. The standard RAG pattern: embed query → similarity_search → inject top-k docs into prompt → generate answer. `OpenAIEmbeddings` converts text to vectors using OpenAI's embedding API.

## ReAct Pattern
ReAct (Reasoning + Acting) is the foundational agent pattern. The LLM alternates between Thought (reasoning about what to do), Action (calling a tool), and Observation (reading the tool's result). This loop continues until the LLM produces a Final Answer. Tool-calling models (function calling) implement ReAct more reliably than text-based parsing.

## LangChain Expression Language (LCEL)
LCEL is LangChain's declarative composition syntax. Components expose `.invoke()`, `.stream()`, `.batch()`, and `.ainvoke()` / `.astream()` for async. Piping with `|` creates a `RunnableSequence`. `RunnablePassthrough` forwards inputs unchanged. LCEL chains are automatically traced in LangSmith.
