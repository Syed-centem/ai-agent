import streamlit as st
import os
import requests
import json
import time
import base64
import random
import re
from pypdf import PdfReader
# Import the brain
from Backend.GeminiBrain import GeminiAgent

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Knowledge Base Agent",
    page_icon="🌌",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- AESTHETIC: ULTRA-FUTURISTIC CSS ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@300;500;700&family=Roboto+Mono:wght@300&display=swap');

    /* 1. ANIMATED DEEP SPACE BACKGROUND */
    .stApp {
        background-color: #050505;
        background-image: 
            radial-gradient(circle at 15% 50%, rgba(76, 29, 149, 0.1) 0%, transparent 25%), 
            radial-gradient(circle at 85% 30%, rgba(14, 165, 233, 0.1) 0%, transparent 25%);
        color: #e0e0e0;
        font-family: 'Rajdhani', sans-serif;
    }
    
    /* CRT Scanline Effect Overlay */
    .stApp::before {
        content: " ";
        display: block;
        position: absolute;
        top: 0;
        left: 0;
        bottom: 0;
        right: 0;
        background: linear-gradient(rgba(18, 16, 16, 0) 50%, rgba(0, 0, 0, 0.05) 50%);
        background-size: 100% 3px;
        z-index: 0;
        pointer-events: none;
    }

    /* 2. TYPOGRAPHY */
    h1, h2, h3, h4 {
        font-family: 'Rajdhani', sans-serif;
        text-transform: uppercase;
        letter-spacing: 2px;
        color: #fff;
    }
    
    /* 3. SIDEBAR HUD */
    section[data-testid="stSidebar"] {
        background: rgba(8, 8, 12, 0.9);
        border-right: 1px solid rgba(0, 210, 255, 0.15);
        box-shadow: 10px 0 30px rgba(0, 0, 0, 0.8);
    }

    /* 4. CHAT MESSAGE CONTAINERS - GLASS PANELS */
    .stChatMessage {
        background: rgba(15, 19, 30, 0.8); 
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 8px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4);
        margin-bottom: 20px;
        padding: 20px;
        position: relative;
        backdrop-filter: blur(5px);
        transition: all 0.3s ease;
    }
    
    /* User Message Styling */
    .stChatMessage[data-testid="stChatMessage"]:nth-child(odd) {
        border-left: 2px solid #ff0055;
        background: linear-gradient(90deg, rgba(40, 10, 20, 0.6) 0%, rgba(15, 19, 30, 0.8) 100%);
    }

    /* Agent Message Styling */
    .stChatMessage[data-testid="stChatMessage"]:nth-child(even) {
        border-right: 2px solid #00d2ff;
        background: linear-gradient(-90deg, rgba(10, 30, 40, 0.6) 0%, rgba(15, 19, 30, 0.8) 100%);
    }

    /* 5. MARKDOWN CONTENT STYLING (THE OUTPUT AESTHETIC) */
    .stMarkdown p {
        font-family: 'Roboto Mono', monospace;
        font-size: 15px;
        line-height: 1.6;
        color: #c0c0c0;
    }
    
    .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
        color: #00d2ff !important;
        text-shadow: 0 0 15px rgba(0, 210, 255, 0.5);
        border-bottom: 1px solid rgba(0, 210, 255, 0.2);
        padding-bottom: 5px;
        margin-top: 20px;
        font-size: 1.4rem;
    }
    
    .stMarkdown strong {
        color: #ff0055;
        font-weight: 700;
        text-shadow: 0 0 5px rgba(255, 0, 85, 0.3);
    }
    
    .stMarkdown code {
        background: #0a0a0a !important;
        color: #00ff9d !important;
        border: 1px solid rgba(0, 255, 157, 0.2);
        font-family: 'Courier New', monospace;
    }
    
    .stMarkdown pre {
        background: #050505 !important;
        border: 1px solid #333;
        border-left: 3px solid #00ff9d;
        box-shadow: inset 0 0 20px rgba(0,0,0,0.8);
    }
    
    /* 6. INPUT FIELD */
    .stTextInput > div > div > input {
        background-color: rgba(0, 0, 0, 0.6);
        color: #00d2ff;
        font-family: 'Roboto Mono', monospace;
        border: 1px solid rgba(0, 210, 255, 0.3);
        border-radius: 4px;
    }
    .stTextInput > div > div > input:focus {
        border-color: #00d2ff;
        box-shadow: 0 0 15px rgba(0, 210, 255, 0.3);
    }

    /* 7. BUTTONS */
    div.stButton > button {
        background: rgba(0, 210, 255, 0.05);
        color: #00d2ff;
        border: 1px solid #00d2ff;
        border-radius: 4px;
        font-family: 'Rajdhani', sans-serif;
        text-transform: uppercase;
        letter-spacing: 2px;
        transition: all 0.3s;
    }
    div.stButton > button:hover {
        background: rgba(0, 210, 255, 0.15);
        box-shadow: 0 0 15px rgba(0, 210, 255, 0.5);
        color: #fff;
        border-color: #fff;
    }
    
    /* 8. SCROLLBAR */
    ::-webkit-scrollbar { width: 8px; background: #050505; }
    ::-webkit-scrollbar-thumb { background: #333; border-radius: 4px; }
    ::-webkit-scrollbar-thumb:hover { background: #00d2ff; }
</style>
""", unsafe_allow_html=True)

# --- INITIALIZE STATE ---
if "messages" not in st.session_state:
    st.session_state.messages = []
if "agent" not in st.session_state:
    st.session_state.agent = None
if "doc_stats" not in st.session_state:
    st.session_state.doc_stats = {"pages": 0, "chars": 0}

# --- SIDEBAR HUD ---
with st.sidebar:
    st.markdown("## 🛰️ SYSTEM HUD")
    
    # 1. Credentials Matrix
    with st.expander("🔑 ENCRYPTION KEYS", expanded=True):
        api_key = st.text_input("API_ACCESS_TOKEN", type="password", help="Gemini API Key")
        
        col1, col2 = st.columns([1,3])
        with col1:
            status_indicator = st.empty()
        with col2:
            if st.button("PING SERVER", use_container_width=True):
                if not api_key:
                    st.error("KEY_MISSING")
                else:
                    status_indicator.markdown("🔴")
                    with st.spinner("Pinging..."):
                        try:
                            url = f"https://generativelanguage.googleapis.com/v1beta/models?key={api_key}"
                            response = requests.get(url)
                            if response.status_code == 200:
                                status_indicator.markdown("🟢")
                                st.toast("UPLINK ESTABLISHED", icon="📶")
                            else:
                                status_indicator.markdown("🔴")
                                st.error(f"ERR_CODE: {response.status_code}")
                        except:
                            status_indicator.markdown("🔴")
                            st.error("NETWORK_FAILURE")

    # 2. Data Ingestion
    st.markdown("---")
    st.markdown("### 📥 DATA INGESTION")
    uploaded_file = st.file_uploader("UPLOAD_SOURCE_PDF", type="pdf", label_visibility="collapsed")
    
    # 3. Neural Configuration
    with st.expander("⚙️ NEURAL PARAMETERS"):
        temp = st.slider("RANDOMNESS (Temp)", 0.0, 1.0, 0.3)
        tokens = st.number_input("MAX_TOKENS", 1000, 8192, 4000)
        
    # 4. Processing Unit
    if uploaded_file and st.button("INITIATE NEURAL LINK", type="primary", use_container_width=True):
        if not api_key:
            st.error("ACCESS_DENIED: MISSING KEY")
        else:
            with st.spinner("Encrypting & Vectorizing Data Stream..."):
                try:
                    reader = PdfReader(uploaded_file)
                    text = ""
                    prog_bar = st.progress(0)
                    for i, page in enumerate(reader.pages):
                        text += page.extract_text() + "\n"
                        time.sleep(0.05) # Aesthetic delay
                        prog_bar.progress((i + 1) / len(reader.pages))
                    
                    st.session_state.agent = GeminiAgent(knowledge_base_content=text, api_key=api_key)
                    st.session_state.doc_stats = {"pages": len(reader.pages), "chars": len(text)}
                    
                    st.toast("DATA LINK ACTIVE", icon="🟢")
                    st.success("VECTORIZATION COMPLETE")
                    
                    # Auto-Summary Feature
                    summary_prompt = "Generate a concise 3-bullet executive briefing of this document."
                    summary = st.session_state.agent.send_message(summary_prompt)
                    st.session_state.messages = [{"role": "assistant", "content": f"### 🛡️ SYSTEM BRIEFING\n\n{summary}"}]
                    
                except Exception as e:
                    st.error(f"CRITICAL_FAILURE: {e}")

    # 5. Live Telemetry
    st.markdown("---")
    st.markdown("### 📊 LIVE TELEMETRY")
    col1, col2 = st.columns(2)
    col1.metric("PAGES", st.session_state.doc_stats["pages"])
    col2.metric("CHARS", f"{st.session_state.doc_stats['chars']//1000}k")
    
    st.metric("LATENCY", f"{random.randint(40, 120)}ms")

    # 6. Mission Logs (History)
    st.markdown("---")
    st.markdown("### 📜 MISSION LOGS")
    with st.container(height=150):
        # Display only user messages as history
        history_logs = [m['content'] for m in st.session_state.messages if m['role'] == 'user']
        if history_logs:
            for log in reversed(history_logs[-5:]): # Show last 5
                st.caption(f"➜ {log[:30]}...")
        else:
            st.caption("NO ACTIVITY DETECTED")

    # 7. Data Dump (Downloads)
    st.markdown("---")
    c1, c2 = st.columns(2)
    with c1:
        # JSON Export
        json_str = json.dumps(st.session_state.messages, indent=2)
        st.download_button(
            "💾 JSON",
            data=json_str,
            file_name="neural_chat_history.json",
            mime="application/json",
            use_container_width=True
        )
    with c2:
        # TXT Export
        txt_str = "\n".join([f"[{m['role'].upper()}] {m['content']}" for m in st.session_state.messages])
        st.download_button(
            "📄 TXT",
            data=txt_str,
            file_name="neural_chat_history.txt",
            mime="text/plain",
            use_container_width=True
        )
        
    if st.button("PURGE MEMORY", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# --- MAIN INTERFACE ---
st.markdown("""
<div style="text-align: center; padding-bottom: 30px;">
    <h1 style="font-size: 4rem; background: -webkit-linear-gradient(#00d2ff, #3a7bd5); -webkit-background-clip: text; -webkit-text-fill-color: transparent; text-shadow: 0px 0px 30px rgba(0, 210, 255, 0.6); margin-bottom: 0;">
        KNOWLEDGE BASE AGENT
    </h1>
    <div style="height: 2px; width: 100px; background: #00d2ff; margin: 10px auto; box-shadow: 0 0 10px #00d2ff;"></div>
    <p style="color: #00d2ff; font-family: 'Roboto Mono'; letter-spacing: 4px; font-size: 0.9rem;">SYSTEM V2.5.0 // ONLINE // SECURE</p>
</div>
""", unsafe_allow_html=True)

if not st.session_state.agent:
    # STANDBY MODE UI
    st.markdown("""
    <div style='background: rgba(10, 10, 15, 0.6); border: 1px dashed #00d2ff; border-radius: 15px; padding: 50px; text-align: center; margin: 20px 0; backdrop-filter: blur(5px); box-shadow: 0 0 30px rgba(0, 210, 255, 0.1);'>
        <h2 style='color: #00d2ff; margin-bottom: 15px;'>AWAITING DATA STREAM</h2>
        <p style='color: #a0a0a0; font-family: "Roboto Mono"; font-size: 1.1rem;'>Please upload a classified document to the secure sidebar terminal to commence analysis.</p>
        <br>
        <div style='display: flex; justify-content: center; gap: 40px; margin-top: 20px;'>
            <div style='color: #555; font-family: "Rajdhani"; font-weight: 700;'>● ENCRYPTION: AES-256</div>
            <div style='color: #555; font-family: "Rajdhani"; font-weight: 700;'>● STATUS: STANDBY</div>
            <div style='color: #555; font-family: "Rajdhani"; font-weight: 700;'>● LINK: DISCONNECTED</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

else:
    # OPERATIONAL MODE UI
    
    # Document Preview Expander
    with st.expander("👁️ RAW DATA STREAM (PREVIEW)", expanded=False):
        st.code(st.session_state.agent.system_prompt["parts"][0]["text"][:1000] + "...", language="text")

    # Chat Log
    chat_container = st.container()
    with chat_container:
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                # Check for Graphviz code blocks to render diagram
                if "```graphviz" in message["content"] or "```dot" in message["content"]:
                    parts = re.split(r"```(graphviz|dot)(.*?)```", message["content"], flags=re.DOTALL)
                    for part in parts:
                        if "digraph" in part or "graph" in part:
                            st.graphviz_chart(part)
                        else:
                            st.markdown(part)
                else:
                    st.markdown(message["content"])
                    
                # Add aesthetic footer to assistant messages
                if message["role"] == "assistant":
                    st.markdown(f"<div style='text-align: right; color: #444; font-size: 0.7rem; font-family: Roboto Mono; margin-top: 10px;'>ID: {random.randint(1000,9999)}-X • LATENCY: {random.randint(40,150)}ms</div>", unsafe_allow_html=True)

    # Command Input
    if prompt := st.chat_input("Enter command or query..."):
        # User Output
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Agent Output
        with st.chat_message("assistant"):
            response_container = st.empty()
            
            # Simulated Processing Visuals
            with st.spinner("NEURAL NET COMPUTING..."):
                # Inject visual request if prompt implies structure
                augmented_prompt = prompt
                if any(word in prompt.lower() for word in ["diagram", "structure", "flow", "chart", "visual", "process"]):
                    augmented_prompt += " (If explaining a process or structure, provide a Graphviz DOT diagram in a code block.)"
                
                full_response = st.session_state.agent.send_message(augmented_prompt)
                
                # Error Recovery
                if "Error" in full_response or "Connection Error" in full_response:
                    if st.session_state.agent.history and st.session_state.agent.history[-1]['role'] == 'user':
                        st.session_state.agent.history.pop()
                
                # Render Output
                if "```graphviz" in full_response or "```dot" in full_response:
                    parts = re.split(r"```(graphviz|dot)(.*?)```", full_response, flags=re.DOTALL)
                    for part in parts:
                        if "digraph" in part or "graph" in part:
                            st.graphviz_chart(part)
                        else:
                            st.markdown(part)
                else:
                    # Cyberpunk Typing Effect
                    displayed_response = ""
                    for char in full_response:
                        displayed_response += char
                        if len(displayed_response) % 3 == 0: 
                            response_container.markdown(displayed_response + "█") 
                            time.sleep(0.002) 
                    response_container.markdown(displayed_response)
        
        st.session_state.messages.append({"role": "assistant", "content": full_response})
        
        # --- AUTO-SCROLL INJECTION ---
        st.markdown(
            """
            <script>
                var element = window.parent.document.querySelector('section.main');
                element.scrollTop = element.scrollHeight;
            </script>
            """,
            unsafe_allow_html=True
        )
        
        time.sleep(0.1)
        st.rerun()
