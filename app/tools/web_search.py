import os
from langchain.tools import tool
from tavily import TavilyClient


@tool
def web_search(query: str) -> str:
    """Search the web for current information, news, facts, or anything requiring
    up-to-date knowledge. Input should be a clear search query."""
    try:
        client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
        results = client.search(query=query, max_results=5)
        if not results.get("results"):
            return "No results found."
        lines = []
        for r in results["results"]:
            lines.append(f"**{r['title']}**\n{r['content']}\nSource: {r['url']}")
        return "\n\n".join(lines)
    except Exception as exc:
        return f"Search error: {exc}"
