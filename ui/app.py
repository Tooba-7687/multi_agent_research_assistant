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
    .main-title {
        font-size: 2.5rem;
        font-weight: 700;
        color: #e0e0e0;
        text-align: center;
        padding: 1rem 0;
    }
    .subtitle {
        font-size: 1.1rem;
        color: #aaa;
        text-align: center;
        margin-bottom: 2rem;
    }
    .agent-card {
        background: #23272f;
        border-left: 4px solid #4CAF50;
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
    }
    .agent-card h4 {
        color: #ffffff;
        margin: 0 0 0.5rem 0;
    }
    .agent-card p {
        color: #ccc;
        margin: 0;
    }
    .success-box {
        background: #1e3a2f;
        border: 1px solid #2d6a4f;
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
        color: #d4edda;
    }
    .error-box {
        background: #3a1e1e;
        border: 1px solid #6a2d2d;
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
        color: #f8d7da;
    }
    </style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────
st.markdown('<div class="main-title">🤖 Multi-Agent Research Assistant</div>',
            unsafe_allow_html=True)
st.markdown('<div class="subtitle">Powered by Google Gemini + Tavily Search | 3 AI Agents working together</div>',
            unsafe_allow_html=True)

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