# LangChain Reference — Chicken Joe's Agent Toolkit

Dude, LangChain is basically the surfboard of AI development. It connects all the gnarly pieces together — the LLM, the tools, the memory, the prompts — so you can build something that actually shreds.

## What is LangChain?

LangChain is an open-source Python (and JS) framework for building applications powered by large language models. It gives you:
- Standardized interfaces for LLMs, embeddings, and vector stores
- A tool/agent system for building ReAct-style agents
- Memory management for multi-turn conversations
- Document loaders and text splitters for RAG pipelines

## Core Components

### LLMs and Chat Models

```python
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0, streaming=True)
```

`temperature=0` means precise and focused — no creative wipeouts. Higher temperature = more creative/random output.

### Tools

Tools are the moves in your surfing repertoire, bro. You define them with the `@tool` decorator:

```python
from langchain.tools import tool

@tool
def shred_calculator(expression: str) -> str:
    """Calculate gnarly math expressions for wave stats."""
    # implementation here
    return result
```

The docstring is critical — the LLM reads it to decide when to use the tool.

### Prompts and ChatPromptTemplate

```python
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are Chicken Joe, a surfing AI agent..."),
    MessagesPlaceholder("chat_history", optional=True),
    ("human", "{input}"),
    MessagesPlaceholder("agent_scratchpad"),
])
```

`MessagesPlaceholder("agent_scratchpad")` is where the agent's ReAct reasoning loop lives — the thoughts, tool calls, and observations.

### Agents

In LangChain Classic (v1.x), you build agents like this:

```python
from langchain_classic.agents import AgentExecutor, create_openai_tools_agent

agent = create_openai_tools_agent(llm, tools, prompt)
executor = AgentExecutor(agent=agent, tools=tools, max_iterations=5)
```

`AgentExecutor` runs the ReAct loop: the agent thinks, calls a tool, observes the result, repeats until it has an answer.

### Memory / Conversation History

LangChain doesn't manage memory automatically — you pass it manually as `chat_history`:

```python
from langchain_core.messages import HumanMessage, AIMessage

history = []
history.append(HumanMessage(content="Who's the best surfer?"))
history.append(AIMessage(content="Kelly Slater, dude."))

# Pass to agent
result = executor.invoke({"input": "What did you just say?", "chat_history": history})
```

### Streaming with astream_events

For real-time token streaming (the surfer way — live, not buffered):

```python
async for event in executor.astream_events({"input": message}, version="v2"):
    if event["event"] == "on_chat_model_stream":
        chunk = event["data"]["chunk"]
        if chunk.content:
            yield chunk.content  # stream each token as it arrives
    elif event["event"] == "on_tool_start":
        tool_name = event["name"]  # show which tool is being used
```

`version="v2"` is required for the newer event format. Don't forget it or things get weird.

## Vector Stores with LangChain-Chroma

```python
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
import chromadb

client = chromadb.EphemeralClient()  # in-memory, resets on restart
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

store = Chroma(
    client=client,
    collection_name="surf_knowledge",
    embedding_function=embeddings,
)

store.add_documents(documents)
results = store.similarity_search(query, k=3)
```

Each result has `.page_content` (the text chunk) and `.metadata` (source file, chunk index, etc.).

## Document Objects

LangChain's `Document` class holds a chunk of text plus metadata:

```python
from langchain_core.documents import Document

doc = Document(
    page_content="Chicken Joe once rode a 40-foot wave on a corn surfboard.",
    metadata={"source": "chicken_joe_biography.md", "chunk": 0}
)
```

The metadata `source` field is what powers source attribution in RAG responses.

## Key LangChain Packages

| Package | What it does |
|---|---|
| `langchain` | Core agent and chain logic |
| `langchain-core` | Base classes, prompts, documents |
| `langchain-openai` | ChatOpenAI, OpenAIEmbeddings |
| `langchain-community` | 100+ integrations (Tavily, etc.) |
| `langchain-chroma` | Chroma vector store integration |
| `langchain-classic` | Legacy AgentExecutor, classic agents |

## Common Gotchas

- **`args` in extra logging** — Python's LogRecord reserves `args`; use `tool_args` instead
- **`AgentExecutor` moved** — in LangChain 1.x, import from `langchain_classic.agents`
- **`astream_events` needs `version="v2"`** — or you get the old event format
- **EphemeralClient resets on restart** — use `PersistentClient` for production surf shacks
