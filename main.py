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


def web_search(query: str):

    try:
        result = tavily.search(query=query, max_results=5)

        results = []

        for r in result["results"]:
            results.append({
                "title": r["title"],
                "url": r["url"],
                "content": r["content"]
            })

        return json.dumps(results)

    except Exception as e:
        return json.dumps({"error": str(e)})


def fetch_webpage(url: str):

    try:
        r = requests.get(url, timeout=10)# dowload page 

        soup = BeautifulSoup(r.text, "html.parser")

        text = soup.get_text()

        return json.dumps({
            "url": url,
            "content": text[:3000]
        })

    except Exception as e:
        return json.dumps({"error": str(e)})


# -----------------------------
# Chat Endpoint
# -----------------------------

@app.get("/chat")
def chat(message: str):

    messages = [
        HumanMessage(
            content=f"""
You are a web search assistant.

Rules:
- Use web_search to find information.
- If needed open webpages using fetch_webpage.
- Always include source URLs in the answer.

User question:
{message}
"""
        )
    ]

    response = llm.invoke(messages)

    # If tool is called
    if response.tool_calls:

        tool_call = response.tool_calls[0]

        tool_name = tool_call["name"]

        args = tool_call["args"]

        if tool_name == "web_search":
            result = web_search(args["query"])

        elif tool_name == "fetch_webpage":
            result = fetch_webpage(args["url"])

        else:
            result = "Tool not found"

        messages.append(response)

        messages.append(
            ToolMessage(
                content=result,
                tool_call_id=tool_call["id"]
            )
        )

        final_response = llm.invoke(messages)

        return {"answer": final_response.content}

    return {"answer": response.content}