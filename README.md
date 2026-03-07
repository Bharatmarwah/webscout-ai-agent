
# Web Search & Page Summarization Agent 🔍📄

A FastAPI-powered intelligent assistant that combines web search and webpage summarization capabilities using Google's Gemini AI and Tavily search API. The agent can search the web, fetch any webpage, extract its content, and provide AI-powered summaries with source citations.

**Created by Bharat**

## 📋 Overview

This application provides an AI-powered assistant that can:
- **Search the web** for latest information using Tavily API
- **Fetch and extract** content from any webpage
- **Summarize webpage content** intelligently
- **Generate contextual answers** with source URLs
- **Utilize Google's Gemini 2.5 Flash** model for natural language understanding and summarization

## ✨ Features

- **Intelligent Web Search**: Uses Tavily API to search the web and return relevant, up-to-date results
- **Webpage Fetching & Extraction**: Retrieves and parses HTML content from any URL
- **Content Summarization**: AI-powered summarization of webpage content using Gemini 2.5 Flash
- **Source Citations**: Automatically includes source URLs in responses
- **RESTful API**: Simple GET endpoint for easy integration
- **Automatic Tool Selection**: AI decides whether to search or fetch based on user queries
- **Dual-Mode Operation**: Works as both a search engine and a webpage summarizer

## 🛠️ Technology Stack

- **FastAPI**: Modern web framework for building APIs
- **LangChain**: Framework for LLM application development
- **Google Gemini**: AI language model (gemini-2.5-flash)
- **Tavily API**: Web search functionality
- **BeautifulSoup4**: HTML parsing and content extraction
- **Requests**: HTTP library for webpage fetching

## 📦 Installation

### Prerequisites

- Python 3.14 or higher
- Google API Key (for Gemini)
- Tavily API Key

### Setup Steps

1. **Clone or download the repository**
```powershell
cd C:\Users\Bharat\OneDrive\Desktop\WebSearchAgent
```

2. **Create and activate virtual environment**
```powershell
python -m venv websearchenv
.\websearchenv\Scripts\Activate.ps1
```

3. **Install dependencies**
```powershell
pip install -r requirements.txt
```

4. **Set up environment variables**

Create a `.env` file or set environment variables:
```powershell
$env:GOOGLE_API_KEY="your_google_api_key_here"
$env:TAVILY_API_KEY="your_tavily_api_key_here"
```

Or create a `.env` file in the project root:
```
GOOGLE_API_KEY=your_google_api_key_here
TAVILY_API_KEY=your_tavily_api_key_here
```

## 🚀 Usage

### Starting the Server

Run the FastAPI server using uvicorn:

```powershell
uvicorn main:app --reload
```

The server will start at `http://localhost:8000`

### API Endpoints

#### Chat Endpoint

**GET** `/chat`

**Query Parameters:**
- `message` (string, required): The user's question, search query, or URL to summarize

**Example Requests:**

*Web Search Example:*
```
http://localhost:8000/chat?message=What are the latest developments in AI?
```

*Webpage Summarization Example:*
```
http://localhost:8000/chat?message=Summarize this article: https://example.com/article
```

**Example Response:**
```json
{
  "answer": "Based on recent web searches, the latest developments in AI include... [Sources: https://example.com/ai-news]"
}
```

### API Documentation

FastAPI provides automatic interactive API documentation:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🔧 How It Works

1. **User submits a query** via the `/chat` endpoint
2. **LLM analyzes the query** and decides which tools to use
3. **Tool execution**:
   - `web_search`: Searches the web using Tavily API (max 5 results)
   - `fetch_webpage`: Fetches and extracts content from specific URLs
4. **AI generates response** based on tool results with source citations

## 📝 API Keys

### Get Google API Key
1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a new API key
3. Copy the key to your environment variables

### Get Tavily API Key
1. Visit [Tavily](https://tavily.com/)
2. Sign up for an account
3. Generate an API key from the dashboard
4. Copy the key to your environment variables

## 🔍 Tool Descriptions

### web_search
- **Purpose**: Search the web for latest information
- **Parameters**: `query` (string)
- **Returns**: JSON array with titles, URLs, and content snippets
- **Max Results**: 5

### fetch_webpage
- **Purpose**: Fetch and extract content from a specific URL
- **Parameters**: `url` (string)
- **Returns**: JSON object with URL and extracted text (first 3000 characters)
- **Timeout**: 10 seconds

## ⚙️ Configuration

Key configurations in `main.py`:

```python
# LLM Model
model="gemini-2.5-flash"
temperature=0.7

# Search Results
max_results=5

# Webpage Content
content_limit=3000  # characters

# Request Timeout
timeout=10  # seconds
```

## 📊 Project Structure

```
WebSearchAgent/
├── main.py              # Main application file
├── requirements.txt     # Python dependencies
├── websearchenv/        # Virtual environment
└── __pycache__/         # Python cache files
```

## 🛡️ Error Handling

The application includes error handling for:
- API request failures
- Timeout errors (10-second limit)
- Invalid URLs
- Tool execution errors

All errors are returned in JSON format with descriptive messages.

## 🚧 Limitations

- Single-turn conversations only (no conversation history)
- Executes only one tool call per request
- Content truncated to 3000 characters
- Maximum 5 search results per query
- Synchronous operations (blocking I/O)

## 🔐 Security Considerations

- API keys stored in environment variables
- Request timeout prevents hanging connections
- Consider adding input validation for production use
- Implement rate limiting for public deployments

## 🤝 Contributing

This is a personal project. Feel free to fork and modify as needed.

## 📄 License

This project is for educational and personal use.

## 🐛 Troubleshooting

### Common Issues

**Import Errors**
```powershell
pip install -r requirements.txt --upgrade
```

**API Key Errors**
- Verify environment variables are set correctly
- Check API key validity and quotas

**Port Already in Use**
```powershell
uvicorn main:app --reload --port 8001
```

**Module Not Found**
```powershell
# Ensure virtual environment is activated
.\websearchenv\Scripts\Activate.ps1
pip list  # Verify installed packages
```

## 📞 Support

For issues related to:
- **Gemini API**: Visit [Google AI Documentation](https://ai.google.dev/)
- **Tavily API**: Visit [Tavily Documentation](https://docs.tavily.com/)
- **FastAPI**: Visit [FastAPI Documentation](https://fastapi.tiangolo.com/)
- **LangChain**: Visit [LangChain Documentation](https://python.langchain.com/)

## 🎯 Future Enhancements

Potential improvements:
- Multi-turn conversation support
- Conversation memory/history
- Multiple tool call chaining
- Async operations for better performance
- Caching mechanism
- Enhanced error handling
- Input validation and sanitization
- Rate limiting
- Logging system
- Unit tests
- CORS configuration
- Docker support
---

