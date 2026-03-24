import os
from langchain.tools import tool
from tavily import TavilyClient
from app.logger import get_logger, log_tool_call, log_tool_error

_log = get_logger("tool.web_search")


@tool
def web_search(query: str) -> str:
    """Search the web for current information, news, facts, or anything requiring
    up-to-date knowledge. Input should be a clear search query."""
    try:
        client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
        results = client.search(query=query, max_results=5)
        if not results.get("results"):
            log_tool_call(_log, "web_search", {"query": query}, "No results found.")
            return "No results found."
        lines = []
        for r in results["results"]:
            lines.append(f"**{r['title']}**\n{r['content']}\nSource: {r['url']}")
        output = "\n\n".join(lines)
        log_tool_call(_log, "web_search", {"query": query, "num_results": len(results["results"])}, output)
        return output
    except Exception as exc:
        log_tool_error(_log, "web_search", {"query": query}, str(exc))
        return f"Search error: {exc}"
