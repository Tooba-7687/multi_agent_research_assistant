import streamlit as st
import sys
import os

# Add root directory to path so imports work
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pipeline.orchestrator import run_pipeline

# ─────────────────────────────────────────
# PAGE CONFIGURATION
# ─────────────────────────────────────────
st.set_page_config(
    page_title = "Multi-Agent Research Assistant",
    page_icon  = "🤖",
    layout     = "wide"
)

# ─────────────────────────────────────────
# CUSTOM STYLING
# ─────────────────────────────────────────
st.markdown("""
    <style>
    :root {
        color-scheme: dark;
    }
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #111827 45%, #1f2937 100%);
    }
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1200px;
    }
    .main-title {
        font-size: 2.7rem;
        font-weight: 800;
        color: #f8fafc;
        text-align: center;
        padding: 0.2rem 0 0.4rem;
        letter-spacing: 0.02em;
    }
    .subtitle {
        font-size: 1.05rem;
        color: #cbd5e1;
        text-align: center;
        margin-bottom: 0.2rem;
    }
    .hero-card {
        background: rgba(15, 23, 42, 0.82);
        border: 1px solid rgba(148, 163, 184, 0.25);
        border-radius: 18px;
        padding: 1.2rem 1.4rem;
        margin-bottom: 1.3rem;
        box-shadow: 0 8px 30px rgba(0, 0, 0, 0.25);
    }
    .agent-card {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.95), rgba(15, 23, 42, 0.95));
        border: 1px solid rgba(96, 165, 250, 0.25);
        border-left: 5px solid #38bdf8;
        padding: 1rem 1rem 1.1rem;
        border-radius: 14px;
        margin: 0.4rem 0 0.6rem;
        box-shadow: 0 6px 18px rgba(0, 0, 0, 0.2);
    }
    .agent-card h4 {
        color: #f8fafc;
        margin: 0 0 0.45rem 0;
        font-size: 1.04rem;
    }
    .agent-card p {
        color: #cbd5e1;
        margin: 0;
        line-height: 1.45;
    }
    .success-box {
        background: linear-gradient(135deg, rgba(6, 78, 59, 0.95), rgba(4, 47, 46, 0.95));
        border: 1px solid rgba(74, 222, 128, 0.35);
        border-radius: 12px;
        padding: 1rem 1.1rem;
        margin: 1rem 0;
        color: #dcfce7;
        box-shadow: 0 6px 18px rgba(0, 0, 0, 0.18);
    }
    .error-box {
        background: linear-gradient(135deg, rgba(69, 10, 10, 0.95), rgba(127, 29, 29, 0.95));
        border: 1px solid rgba(248, 113, 113, 0.35);
        border-radius: 12px;
        padding: 1rem 1.1rem;
        margin: 1rem 0;
        color: #fee2e2;
        box-shadow: 0 6px 18px rgba(0, 0, 0, 0.18);
    }
    div[data-testid="stTextInput"] input,
    div[data-testid="stTextInput"] textarea {
        background-color: #111827 !important;
        color: #f8fafc !important;
        border: 1px solid #475569 !important;
        border-radius: 10px !important;
    }
    div[data-testid="stTextInput"] label,
    div[data-testid="stSelectbox"] label {
        color: #e2e8f0 !important;
    }
    div[data-testid="stSelectbox"] div[data-baseweb="select"] > div {
        background-color: #111827 !important;
        color: #f8fafc !important;
        border: 1px solid #475569 !important;
    }
    .stButton > button,
    .stDownloadButton > button {
        background: linear-gradient(135deg, #2563eb, #38bdf8);
        color: white;
        border: none;
        border-radius: 999px;
        padding: 0.6rem 1rem;
        font-weight: 700;
        box-shadow: 0 6px 18px rgba(37, 99, 235, 0.25);
    }
    .stButton > button:hover,
    .stDownloadButton > button:hover {
        background: linear-gradient(135deg, #1d4ed8, #0ea5e9);
        color: white;
    }
    .stMarkdown {
        color: #f8fafc;
    }
    .stMarkdown h1,
    .stMarkdown h2,
    .stMarkdown h3,
    .stMarkdown h4 {
        color: #f8fafc;
    }
    .stMarkdown p,
    .stMarkdown li {
        color: #e2e8f0;
        line-height: 1.6;
    }
    </style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────
st.markdown("""
<div class="hero-card">
    <div class="main-title">🤖 Multi-Agent Research Assistant</div>
    <div class="subtitle">Powered by Google Gemini + Tavily Search | 3 AI Agents working together</div>
</div>
""", unsafe_allow_html=True)

st.divider()

# ─────────────────────────────────────────
# AGENT PIPELINE OVERVIEW
# ─────────────────────────────────────────
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="agent-card">
        <h4>🔍 Research Agent</h4>
        <p>Searches the web & extracts raw information using Tavily</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="agent-card">
        <h4>📝 Summarizer Agent</h4>
        <p>Analyzes & structures the raw data into key points</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="agent-card">
        <h4>✍️ Writer Agent</h4>
        <p>Writes a polished, full research report</p>
    </div>
    """, unsafe_allow_html=True)

st.divider()

# ─────────────────────────────────────────
# USER INPUT SECTION
# ─────────────────────────────────────────
st.subheader("📌 Enter Your Research Topic")

query = st.text_input(
    label       = "Research Topic",
    placeholder = "e.g. Impact of AI on healthcare in 2024",
    label_visibility = "collapsed"
)

col_tone, col_btn = st.columns([2, 1])

with col_tone:
    tone = st.selectbox(
        "Select Writing Tone",
        options = ["professional", "academic", "casual"],
        index   = 0
    )

with col_btn:
    st.write("")
    run_button = st.button(
        "🚀 Generate Report",
        use_container_width = True,
        type = "primary"
    )

st.divider()

# ─────────────────────────────────────────
# PIPELINE EXECUTION
# ─────────────────────────────────────────
if run_button:
    if not query.strip():
        st.error("⚠️ Please enter a research topic first!")
    else:
        # Progress tracking
        st.subheader("⚙️ Pipeline Running...")
        progress_bar = st.progress(0)
        status_text  = st.empty()

        with st.spinner("🤖 Agents are working..."):

            # Update progress steps
            status_text.text("🔍 Research Agent is searching the web...")
            progress_bar.progress(10)

            # Run the full pipeline
            result = run_pipeline(query=query, tone=tone)

            progress_bar.progress(100)
            status_text.text("✅ All agents completed!")

        st.divider()

        # ─────────────────────────────────────────
        # DISPLAY RESULTS
        # ─────────────────────────────────────────
        if result["status"] == "success":

            # Success message
            st.markdown(f"""
            <div class="success-box">
                ✅ <strong>Report Generated Successfully!</strong>
                &nbsp;|&nbsp; ⏱️ Time: {result['duration']} seconds
                &nbsp;|&nbsp; 🎨 Tone: {result['tone'].capitalize()}
            </div>
            """, unsafe_allow_html=True)

            # Report display
            st.subheader("📄 Your Research Report")
            st.markdown(result["report"])

            st.divider()

            # Sources section
            if result["sources"]:
                st.subheader("🔗 Sources Used")
                for i, source in enumerate(result["sources"], 1):
                    st.markdown(f"{i}. [{source['title']}]({source['url']})")

            st.divider()

            # Download button
            st.download_button(
                label    = "⬇️ Download Report as .txt",
                data     = result["report"],
                file_name = f"research_{query[:20].replace(' ','_')}.txt",
                mime     = "text/plain"
            )

        else:
            # Error display
            st.markdown(f"""
            <div class="error-box">
                ❌ <strong>Pipeline Failed</strong>
                at step: <strong>{result.get('step', 'unknown')}</strong><br>
                Error: {result.get('error', 'Unknown error')}
            </div>
            """, unsafe_allow_html=True)

# ─────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────
st.divider()
st.markdown("""
    <div style='text-align:center; color:#888; font-size:0.85rem;'>
        Built by Tooba Nadeem &nbsp;|&nbsp; 
        Multi-Agent AI System &nbsp;|&nbsp; 
        Powered by Gemini + Tavily
    </div>
""", unsafe_allow_html=True)