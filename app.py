import streamlit as st
import requests
import json
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Web Search Agent",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom styling
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stTextInput > div > div > input {
        font-size: 16px;
    }
    .response-box {
        background-color: #f0f2f6;
        padding: 1.5rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
    .source-link {
        display: inline-block;
        background-color: #e3f2fd;
        padding: 0.5rem 1rem;
        border-radius: 4px;
        margin: 0.25rem;
        text-decoration: none;
    }
    .error-box {
        background-color: #ffebee;
        padding: 1rem;
        border-radius: 8px;
        color: #c62828;
        border-left: 4px solid #c62828;
    }
    .success-box {
        background-color: #e8f5e9;
        padding: 1rem;
        border-radius: 8px;
        color: #2e7d32;
        border-left: 4px solid #2e7d32;
    }
    </style>
""", unsafe_allow_html=True)

# Header
st.title("🔍 Web Search & Page Summarization Agent")
st.markdown("Build by Bharat | Powered by LangChain, Google Gemini & FastAPI")
st.markdown("---")

# Sidebar configuration
with st.sidebar:
    st.header("⚙️ Configuration")

    api_url = st.text_input(
        "API Base URL",
        value="http://localhost:8000",
        help="Enter your FastAPI backend URL"
    )

    st.markdown("---")
    st.subheader("📝 Usage Tips")
    st.markdown("""
    - **Ask anything**: Search queries or questions
    - **Get sources**: Links to original content
    - **Smart fetching**: AI decides when to search or fetch pages
    - **Max 3 steps**: To prevent infinite loops
    """)

    st.markdown("---")
    st.subheader("🔗 Links")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("[📚 GitHub](https://github.com/Bharatmarwah)")

    with col2:
        st.markdown("[💬 Email](mailto:bharatmarwah4@gmail.com)")

# Main interface
col1, col2 = st.columns([3, 1], gap="large")

with col1:
    st.subheader("Ask Your Question")
    user_query = st.text_area(
        "Enter your search query or question:",
        placeholder="e.g., What are the latest developments in AI in 2026?",
        height=100,
        label_visibility="collapsed"
    )

with col2:
    st.subheader("Options")
    show_details = st.checkbox("Show request details", value=False)
    clear_cache = st.button("Clear History", use_container_width=True)

# Session state for history
if "history" not in st.session_state:
    st.session_state.history = []

# Submit button
col1, col2, col3 = st.columns([1, 1, 1])

with col1:
    submit_btn = st.button("🔍 Search", use_container_width=True, type="primary")

with col2:
    if clear_cache:
        st.session_state.history = []
        st.success("History cleared!")
        st.rerun()

# Process request
if submit_btn and user_query.strip():
    if show_details:
        st.info("Processing your request...")

    with st.spinner("🔄Looking for the best answer..."):
        try:
            # Make API request
            response = requests.get(
                f"{api_url}/chat",
                params={"message": user_query},
                timeout=30
            )

            if response.status_code == 200:
                data = response.json()
                answer = data.get("answer", "No response received")

                # Store in history
                st.session_state.history.insert(0, {
                    "query": user_query,
                    "answer": answer,
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                })

                # Display response
                st.markdown("---")
                st.subheader("📊 Response")

                with st.container():
                    st.markdown(f"""
                    <div class="response-box">
                    {answer}
                    </div>
                    """, unsafe_allow_html=True)

                # Extract and display sources
                if "Sources:" in answer:
                    st.markdown("**📌 Sources:**")
                    sources_section = answer.split("Sources:")[-1].strip()
                    for line in sources_section.split("\n"):
                        if line.strip().startswith("-"):
                            url = line.strip().lstrip("- ").strip()
                            if url.startswith("http"):
                                st.markdown(f"🔗 [{url}]({url})")

                if show_details:
                    st.success("✅ Request completed successfully!")
            else:
                st.markdown("""
                <div class="error-box">
                ❌ API Error: Server returned status code 
                """ + str(response.status_code) + """
                </div>
                """, unsafe_allow_html=True)

        except requests.exceptions.ConnectionError:
            st.markdown("""
            <div class="error-box">
            ❌ Connection Error: Cannot reach the API server.
            <br/>Make sure the FastAPI server is running at: """ + api_url + """
            </div>
            """, unsafe_allow_html=True)
        except requests.exceptions.Timeout:
            st.markdown("""
            <div class="error-box">
            ⏱️ Timeout Error: The request took too long to complete.
            </div>
            """, unsafe_allow_html=True)
        except Exception as e:
            st.markdown(f"""
            <div class="error-box">
            ❌ Error: {str(e)}
            </div>
            """, unsafe_allow_html=True)

# Display history
if st.session_state.history:
    st.markdown("---")
    st.subheader("📜 Search History")

    for idx, item in enumerate(st.session_state.history):
        with st.expander(f"🕐 {item['timestamp']} - {item['query'][:60]}..."):
            st.markdown("**Query:**")
            st.code(item['query'])
            st.markdown("**Response:**")
            st.markdown(item['answer'])

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #888; font-size: 12px;">
Created by Bharat | Powered by FastAPI, LangChain & Google Gemini
</div>
""", unsafe_allow_html=True)

