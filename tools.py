from langchain_core.tools import tool
import requests
from bs4 import BeautifulSoup
from tavily import TavilyClient
import os
from dotenv import load_dotenv

load_dotenv()

tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

@tool
def web_search(query: str) -> str:
    """Search the web for recent and reliable information on a topic and return results."""
    result = tavily.search(query=query, max_results=5)
    out = []
    for r in result['results']:
        out.append(
            f"title: {r['title']}\nURL: {r['url']}\nSnippet: {r['content'][:300]}\n"
        )
    return "\n----\n".join(out)

@tool
def scrape_url(url: str) -> str:
    """Scrape the content of a URL and return the text content from a given URL for deeper reading."""
    try:
        resp = requests.get(url, timeout=8, headers={'User-Agent': 'Mozilla/5.0'})
        soup = BeautifulSoup(resp.text, 'html.parser')
        for tag in soup(['script', 'style', 'header', 'footer', 'nav', 'aside']):
            tag.decompose()
        return soup.get_text(separator='\n', strip=True)[:3000]
    except Exception as e:
        return f"could not scrape URL: {str(e)}"