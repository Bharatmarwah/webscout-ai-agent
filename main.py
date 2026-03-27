from fastapi import FastAPI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, ToolMessage
from tavily import TavilyClient
import requests
from bs4 import BeautifulSoup
import json
import os

app = FastAPI()

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.7,
    google_api_key=os.getenv("GOOGLE_API_KEY")
)

tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

tools = [
    {
        "type": "function",
        "function": {
            "name": "web_search",
            "description": "Search the web for latest information and return URLs",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "search query"
                    }
                },
                "required": ["query"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "fetch_webpage",
            "description": "Fetch the content of a webpage from a URL",
            "parameters": {
                "type": "object",
                "properties": {
                    "url": {
                        "type": "string",
                        "description": "webpage url"
                    }
                },
                "required": ["url"]
            }
        }
    }
]

llm = llm.bind_tools(tools)

def extract_text(content):
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        return " ".join(
            item.get("text", "") for item in content if isinstance(item, dict)
        )
    return str(content)

def web_search(query: str):
    result = tavily.search(query=query, max_results=3)
    return [
        {
            "url": r["url"],
            "title": r["title"],
            "content": r["content"]
        }
        for r in result["results"]
    ]

def fetch_webpage(url: str):
    r = requests.get(url, timeout=5)
    soup = BeautifulSoup(r.text, "html.parser")
    return {
        "url": url,
        "content": soup.get_text()[:3000]
    }

@app.get("/chat")
def chat(message: str):
    messages = [
        HumanMessage(
            content=f"""
You are a web search assistant.

Rules:
- Use web_search to find information.
- Use fetch_webpage if needed.
- Answer ONLY from retrieved data.
- Always include source URLs.

Format:
Answer: <short answer>
Sources:
- <url1>
- <url2>

User question: {message}
"""
        )
    ]

    MAX_STEPS = 3

    for _ in range(MAX_STEPS):
        response = llm.invoke(messages)

        if not response.tool_calls:
            clean = extract_text(response.content).replace("\\n", "\n").strip()
            return {"answer": clean}

        tool_call = response.tool_calls[0]
        tool_name = tool_call["name"]
        args = tool_call["args"]

        try:
            if tool_name == "web_search":
                result = web_search(args["query"])
            elif tool_name == "fetch_webpage":
                result = fetch_webpage(args["url"])
            else:
                result = {"error": "Tool not found"}
        except Exception as e:
            result = {"error": str(e)}

        messages.append(response)
        messages.append(
            ToolMessage(
                content=json.dumps(result),
                tool_call_id=tool_call["id"]
            )
        )

    return {"answer": "Failed to generate response in limited steps"}