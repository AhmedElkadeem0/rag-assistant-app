import streamlit as st
import time
from api_client import query_rag_api, check_backend_health

# Page configuration
st.set_page_config(
    page_title="DocuMind RAG | AI Assistant",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS styling for a modern UI
st.markdown("""
<style>
    /* Global styles */
    .main {
        background-color: #0e1117;
    }
    
    /* Header styling */
    .app-header {
        background: linear-gradient(135deg, #1f2937 0%, #111827 100%);
        padding: 1.8rem;
        border-radius: 12px;
        border: 1px solid #374151;
        margin-bottom: 1.5rem;
    }
    
    .app-title {
        color: #f9fafb;
        font-size: 2.2rem;
        font-weight: 700;
        margin: 0;
        letter-spacing: -0.5px;
    }
    
    .app-subtitle {
        color: #9ca3af;
        font-size: 1rem;
        margin-top: 0.4rem;
    }

    /* Badge tags for sources */
    .source-badge {
        display: inline-block;
        background-color: #1e3a8a;
        color: #93c5fd;
        padding: 0.2rem 0.6rem;
        border-radius: 6px;
        font-size: 0.8rem;
        font-weight: 600;
        margin-right: 0.4rem;
        margin-top: 0.4rem;
        border: 1px solid #1d4ed8;
    }

    /* Custom chat bubbles */
    .stChatMessage {
        border-radius: 10px;
        padding: 1rem;
        margin-bottom: 0.8rem;
    }
</style>
""", unsafe_allow_html=True)

# Custom Header Banner
st.markdown("""
<div class="app-header">
    <div class="app-title">⚡ DocuMind Technical Assistant</div>
    <div class="app-subtitle">Grounded Knowledge Retrieval & Context-Aware Question Answering</div>
</div>
""", unsafe_allow_html=True)

# Sidebar System Dashboard
with st.sidebar:
    st.image("https://img.icons8.com/isometric/100/processor.png", width=64)
    st.title("System Control")
    st.markdown("---")
    
    # Live Health Check
    is_online = check_backend_health()
    if is_online:
        st.success("🟢 **Backend Status:** Online")
    else:
        st.error("🔴 **Backend Status:** Offline")
        st.warning("Ensure FastAPI server is running on `port 8000`.")

    st.markdown("---")
    st.subheader("Model Configuration")
    st.info("**LLM Engine:** Qwen 2.5 (1.5B/3B)")
    st.info("**Vector Database:** ChromaDB Persistent")
    st.info("**Embedding Model:** MiniLM-L6-v2")

    st.markdown("---")
    if st.button("🗑️ Clear Chat History", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# Initialize Chat Session
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display Chat History with Enhanced Source Badges
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if "sources" in msg and msg["sources"]:
            st.markdown("**Retrieved Sources:**")
            badges_html = "".join([f'<span class="source-badge">📄 {src}</span>' for src in msg["sources"]])
            st.markdown(badges_html, unsafe_allow_html=True)

# User Query Processing
if prompt := st.chat_input("Ask a question about your technical documents..."):
    # Render user prompt immediately
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Process response
    with st.chat_message("assistant"):
        start_time = time.time()
        with st.spinner("🔍 Searching vector store & querying local LLM..."):
            result = query_rag_api(prompt)
        elapsed_time = round(time.time() - start_time, 2)

        if "error" in result:
            st.error(result["error"])
        else:
            answer = result.get("answer", "No response generated.")
            sources = result.get("sources", [])

            st.markdown(answer)
            
            # Format sources cleanly as interactive badges
            if sources:
                st.markdown("**Retrieved Sources:**")
                badges_html = "".join([f'<span class="source-badge">📄 {src}</span>' for src in sources])
                st.markdown(badges_html, unsafe_allow_html=True)
                
            st.caption(f"⚡ *Response generated in {elapsed_time}s*")

            # Store message context
            st.session_state.messages.append({
                "role": "assistant",
                "content": answer,
                "sources": sources
            })