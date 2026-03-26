import os
from langchain_classic.agents import AgentExecutor, create_openai_tools_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI

from app.tools.calculator import calculator
from app.tools.web_search import web_search
from app.tools.rag import rag_search

SYSTEM_PROMPT = """You are a helpful AI assistant with access to three tools:
- **Calculator**: evaluate math expressions
- **Web Search**: find current information on the web
- **RAG Search**: search the internal knowledge base documentation

Use the right tool when needed. Be clear and concise."""


def create_agent() -> AgentExecutor:
    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0,
        streaming=True,
        api_key=os.getenv("OPENAI_API_KEY"),
    )
    tools = [calculator, web_search, rag_search]
    prompt = ChatPromptTemplate.from_messages([
        ("system", SYSTEM_PROMPT),
        MessagesPlaceholder("chat_history", optional=True),
        ("human", "{input}"),
        MessagesPlaceholder("agent_scratchpad"),
    ])
    agent = create_openai_tools_agent(llm, tools, prompt)
    return AgentExecutor(agent=agent, tools=tools, handle_parsing_errors=True, max_iterations=5)
