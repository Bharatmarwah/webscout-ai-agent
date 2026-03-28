# Web Search & Page Summarization Agent 🔍📄

A FastAPI-powered intelligent assistant that combines web search, webpage fetching, and AI summarization with a Streamlit frontend for easy interaction.

**Created by Bharat**

- GitHub: https://github.com/Bharatmarwah

## 📋 Overview

This project now has two layers:
- **FastAPI backend** for AI/tool orchestration and API responses
- **Streamlit frontend** for a simple chat-style web UI that calls the backend API

The assistant can:
- Search the web for latest information
- Fetch and extract content from webpages
- Summarize webpage content
- Return contextual answers with source citations

## ✨ Features

- **FastAPI Backend API**: Exposes `/chat` endpoint for query processing
- **Streamlit Frontend**: User-friendly interface to send queries and display answers
- **Intelligent Web Search**: Uses Tavily API for up-to-date results
- **Webpage Fetch + Extraction**: Pulls text content from target URLs
- **AI Summarization**: Uses Gemini 2.5 Flash for concise summaries
- **Source Citations**: Preserves source URLs in responses

## 🛠️ Technology Stack

- **FastAPI**: Backend API service
- **Streamlit**: Frontend web app
- **LangChain**: LLM tooling/orchestration
- **Google Gemini**: AI model (`gemini-2.5-flash`)
- **Tavily API**: Web search
- **BeautifulSoup4**: HTML parsing
- **Requests**: HTTP operations

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

### 1) Start Backend (FastAPI)

```powershell
uvicorn main:app --reload
```

Backend default URL:
- `http://localhost:8000`

### 2) Start Frontend (Streamlit)

```powershell
streamlit run app.py
```

Frontend default URL:
- `http://localhost:8501`

### 3) Use the App

- Open Streamlit in browser
- Enter a query (question, search prompt, or webpage URL request)
- Streamlit sends it to FastAPI `/chat`
- Response is shown in the UI

### API Endpoints

#### Chat Endpoint

**GET** `/chat`

**Query Parameters:**
- `message` (string, required): User query or webpage summarization prompt

**Note on spacing / extra words in query:**
- The API handles normal extra spaces and natural language phrasing.
- For best accuracy, keep prompts clear and specific.

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

## 🔧 How It Works

1. **User submits a query** via the `/chat` endpoint
2. **LLM analyzes the query** and decides which tools to use
3. **Tool execution**:
   - `web_search`: Searches the web using Tavily API (max 5 results)
   - `fetch_webpage`: Fetches and extracts content from specific URLs
4. **AI generates response** based on tool results with source citations

## 🧭 Frontend-Backend Flow

1. User enters prompt in Streamlit (`app.py`)
2. Streamlit sends request to FastAPI backend (`main.py`) at `/chat`
3. Backend chooses tool flow (search/fetch/summarize)
4. Backend returns final answer
5. Streamlit renders the response

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

```text
WebSearchAgent/
├── app.py               # Streamlit frontend
├── main.py              # FastAPI backend
├── README.md            # Project documentation
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

- Email: bharatmarwah4@gmail.com
- GitHub: https://github.com/Bharatmarwah
- Gemini API docs: https://ai.google.dev/
- Tavily API docs: https://docs.tavily.com/
- FastAPI docs: https://fastapi.tiangolo.com/
- Streamlit docs: https://docs.streamlit.io/

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

