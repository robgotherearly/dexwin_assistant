import streamlit as st
from anthropic import Anthropic
import time
from datetime import datetime
import json
from io import BytesIO

# Page config
st.set_page_config(
    page_title="Dexwin Assistant by Robert Marsh Deku",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Ultra-modern CSS with all enhancements
st.markdown("""
<style>
    * {
        margin: 0;
        padding: 0;
    }
    
    html, body, [data-testid="stAppViewContainer"] {
        background: linear-gradient(135deg, #0a0e27 0%, #16213e 50%, #0f3460 100%) !important;
        min-height: 100vh;
        font-family: 'Segoe UI', Trebuchet MS, sans-serif;
    }
    
    .stApp {
        background: transparent !important;
    }
    
    .main {
        background: transparent !important;
    }
    
    @keyframes glow {
        0%, 100% { text-shadow: 0 0 20px rgba(59, 130, 246, 0.5); }
        50% { text-shadow: 0 0 40px rgba(139, 92, 246, 0.8); }
    }
    
    @keyframes slideIn {
        from {
            opacity: 0;
            transform: translateY(10px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes typing {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.5; }
    }
    
    .header-title {
        font-size: 3em;
        font-weight: 900;
        background: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 50%, #ec4899 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 10px;
        letter-spacing: -1px;
        animation: glow 3s ease-in-out infinite;
    }
    
    .header-subtitle {
        font-size: 1.1em;
        color: #cbd5e1;
        font-weight: 300;
        letter-spacing: 0.5px;
    }
    
    .user-msg {
        background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
        color: white;
        padding: 14px 18px;
        border-radius: 16px;
        margin: 10px 0;
        margin-left: auto;
        max-width: 85%;
        width: fit-content;
        box-shadow: 0 8px 24px rgba(59, 130, 246, 0.4);
        animation: slideIn 0.4s ease-out;
        font-weight: 500;
        line-height: 1.5;
    }
    
    .bot-msg {
        background: rgba(30, 41, 59, 0.6);
        color: #e2e8f0;
        padding: 14px 18px;
        border-radius: 16px;
        margin: 10px 0;
        margin-right: auto;
        max-width: 85%;
        width: fit-content;
        border-left: 3px solid #3b82f6;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.3);
        animation: slideIn 0.4s ease-out;
        line-height: 1.6;
    }
    
    .msg-timestamp {
        font-size: 0.8em;
        color: #94a3b8;
        margin-top: 5px;
    }
    
    .msg-actions {
        display: flex;
        gap: 8px;
        margin-top: 8px;
        font-size: 0.9em;
    }
    
    .msg-action-btn {
        cursor: pointer;
        padding: 4px 8px;
        border-radius: 4px;
        background: rgba(59, 130, 246, 0.2);
        color: #3b82f6;
        transition: all 0.2s;
        border: none;
    }
    
    .msg-action-btn:hover {
        background: rgba(59, 130, 246, 0.4);
    }
    
    .typing-indicator {
        display: flex;
        gap: 4px;
        padding: 10px;
    }
    
    .typing-dot {
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background: #3b82f6;
        animation: typing 1.4s infinite;
    }
    
    .typing-dot:nth-child(2) {
        animation-delay: 0.2s;
    }
    
    .typing-dot:nth-child(3) {
        animation-delay: 0.4s;
    }
    
    .stChatInputContainer {
        background: transparent !important;
        border: none !important;
    }
    
    .stChatInput {
        background: rgba(30, 41, 59, 0.5) !important;
        border: 1px solid rgba(148, 163, 184, 0.2) !important;
        color: #e2e8f0 !important;
        border-radius: 14px !important;
        padding: 14px 18px !important;
        font-size: 1em !important;
        backdrop-filter: blur(10px);
        transition: all 0.3s ease !important;
    }
    
    .stChatInput:focus {
        border: 1px solid rgba(59, 130, 246, 0.5) !important;
        box-shadow: 0 0 20px rgba(59, 130, 246, 0.2) !important;
    }
    
    .action-buttons {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 15px;
        margin-top: 25px;
        animation: slideIn 0.6s ease-out 0.2s both;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%) !important;
        color: white !important;
        border: 1px solid rgba(59, 130, 246, 0.5) !important;
        border-radius: 12px !important;
        padding: 14px 24px !important;
        font-weight: 700 !important;
        font-size: 0.95em !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow: 0 8px 24px rgba(59, 130, 246, 0.3) !important;
        cursor: pointer !important;
        backdrop-filter: blur(10px);
    }
    
    .stButton > button:hover {
        transform: translateY(-4px) scale(1.02) !important;
        box-shadow: 0 12px 32px rgba(59, 130, 246, 0.5) !important;
        background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%) !important;
    }
    
    .category-filter {
        display: flex;
        gap: 10px;
        margin: 20px 0;
        flex-wrap: wrap;
    }
    
    .category-btn {
        padding: 8px 16px;
        border-radius: 20px;
        border: 1px solid rgba(59, 130, 246, 0.3);
        background: rgba(59, 130, 246, 0.1);
        color: #3b82f6;
        cursor: pointer;
        transition: all 0.3s;
        font-size: 0.9em;
        font-weight: 600;
    }
    
    .category-btn:hover {
        background: rgba(59, 130, 246, 0.3);
        border-color: rgba(59, 130, 246, 0.6);
    }
    
    .category-btn.active {
        background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
        color: white;
        border-color: #3b82f6;
    }
    
    .stats-bar {
        display: flex;
        gap: 20px;
        padding: 15px;
        background: rgba(30, 41, 59, 0.3);
        border-radius: 12px;
        margin: 15px 0;
        font-size: 0.95em;
        color: #cbd5e1;
    }
    
    .stat-item {
        display: flex;
        align-items: center;
        gap: 8px;
    }
    
    .footer {
        text-align: center;
        color: #94a3b8;
        font-size: 0.95em;
        margin-top: 40px;
        padding-top: 25px;
        border-top: 1px solid rgba(148, 163, 184, 0.1);
        animation: slideIn 0.6s ease-out 0.4s both;
    }
    
    .footer a {
        color: #3b82f6;
        text-decoration: none;
        font-weight: 600;
        transition: color 0.3s ease;
    }
    
    .footer a:hover {
        color: #8b5cf6;
    }
</style>
""", unsafe_allow_html=True)

# Initialize Anthropic client
try:
    api_key = st.secrets["ANTHROPIC_API_KEY"]
except KeyError:
    st.error("⚠️ Please add your Anthropic API key to Streamlit secrets")
    st.stop()

client = Anthropic(api_key=api_key)

# System prompt
SYSTEM_PROMPT = """You are a helpful customer service chatbot for Dexwin Tech Ltd, a digital product development agency based in Ghana.

COMPANY INFORMATION:
- Dexwin is an end-to-end digital product development agency
- Mission: "Empowering Global Innovation Through African Excellence"
- They provide talent to leading firms looking to expand their product teams
- Based in Ghana and expanding globally

CORE SERVICES:
1. Product Design - Intuitive, user-centered interfaces and user experiences
2. Software Development - Scalable web and mobile app solutions using modern frameworks
3. Data Analytics - Actionable insights from raw data to guide decisions
4. Skills Training - Tailored programs to upskill internal teams
5. Talent Outsourcing - Contract-based or embedded team members across roles and stacks
6. IT Consulting - Wide range of general services to support business operations

DELIVERY MODELS:
- End to End Delivery: Full-cycle project execution from concept to launch
- Supplying Extra Hands: Reinforcing teams with skilled professionals on demand
- Embedded Full Teams: Autonomous teams to lead and deliver client vision

NOTABLE PROJECTS:
1. MyMTN App - Transitioned MTN Ghana's USSD into mobile app (1M+ active users, 127% growth)
2. Saving Grains - Hybrid solution for rural farmers (15K+ farmers reached, 500% growth)
3. MTN Pulse - Digital hub for youth engagement (500K+ engaged, 100K+ daily sessions)
4. MTN Hoods - Top-up experience platform (1K+ transactions/day, 3 taps average)

KEY PARTNERSHIPS:
- MTN Ghana (largest telecom provider)
- GIZ (German development agency)
- The World Bank
- Saving Grains (social enterprise)

Be friendly, professional, and helpful. If asked about something not in this knowledge base, be honest and suggest contacting them directly at https://dexwin.net/gh/contact-us or request a quote."""

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "preferences" not in st.session_state:
    st.session_state.preferences = {}
if "start_time" not in st.session_state:
    st.session_state.start_time = time.time()
if "response_times" not in st.session_state:
    st.session_state.response_times = []
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = True
if "selected_category" not in st.session_state:
    st.session_state.selected_category = None

# Header
st.markdown("""
<div style="margin-bottom: 20px;">
    <div class="header-title">✨ Dexwin Assistant by Robert Marsh Deku</div>
    <div class="header-subtitle">Your intelligent guide to transforming ideas into digital excellence</div>
</div>
""", unsafe_allow_html=True)

# Theme toggle
col1, col2 = st.columns([10, 1])
with col2:
    theme_text = "🌙 Dark" if st.session_state.dark_mode else "☀️ Light"
    if st.button(theme_text, key="theme_toggle", help="Toggle dark/light mode"):
        st.session_state.dark_mode = not st.session_state.dark_mode
        st.rerun()

# Action buttons
st.markdown('<div class="action-buttons">', unsafe_allow_html=True)
col1, col2, col3 = st.columns(3)

with col1:
    st.link_button("📞 Contact Us", "https://dexwin.net/gh/contact-us", use_container_width=True)

with col2:
    st.link_button("🎯 Request Quote", "https://dexwin.net/gh/contact-us", use_container_width=True)

with col3:
    st.link_button("🔍 View Projects", "https://dexwin.net/gh/projects", use_container_width=True)

st.markdown('</div>', unsafe_allow_html=True)

# Category filters
st.markdown("**Filter by category:**")
col1, col2, col3, col4, col5, col6 = st.columns(6)

categories = {
    "Services": "Services",
    "Projects": "Projects", 
    "Pricing": "Pricing",
    "Team": "Team",
    "Partners": "Partners",
    "All": None
}

selected = st.session_state.selected_category

cols = [col1, col2, col3, col4, col5, col6]
for i, (label, value) in enumerate(categories.items()):
    with cols[i]:
        if st.button(label, key=f"cat_{label}", use_container_width=True):
            st.session_state.selected_category = value
            st.rerun()

# Chat display with timestamps and actions
for idx, message in enumerate(st.session_state.messages):
    if message["role"] == "user":
        st.markdown(f'<div class="user-msg">{message["content"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="bot-msg">{message["content"]}</div>', unsafe_allow_html=True)

# Input section
user_input = st.chat_input("✍️ Ask me anything about Dexwin...", key="chat_input")

if user_input:
    # Add user message with timestamp
    user_msg = {
        "role": "user",
        "content": user_input,
        "timestamp": datetime.now().strftime("%I:%M %p")
    }
    st.session_state.messages.append(user_msg)
    
    # Show typing indicator
    typing_placeholder = st.empty()
    with typing_placeholder.container():
        st.markdown("""
        <div class="bot-msg">
            <div class="typing-indicator">
                <div class="typing-dot"></div>
                <div class="typing-dot"></div>
                <div class="typing-dot"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Measure response time
    start_response = time.time()
    
    # Stream response
    response_placeholder = st.empty()
    full_response = ""
    
    try:
        with client.messages.stream(
            model="claude-haiku-4-5-20251001",
            max_tokens=1024,
            system=SYSTEM_PROMPT,
            messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages[:-1]] + [{"role": "user", "content": user_input}]
        ) as stream:
            for text in stream.text_stream:
                full_response += text
                response_placeholder.markdown(f'<div class="bot-msg">{full_response}</div>', unsafe_allow_html=True)
    except Exception as e:
        full_response = f"Sorry, I encountered an error: {str(e)}"
        response_placeholder.markdown(f'<div class="bot-msg">{full_response}</div>', unsafe_allow_html=True)
    
    # Calculate response time
    response_time = time.time() - start_response
    st.session_state.response_times.append(response_time)
    
    # Add bot message with metadata
    bot_msg = {
        "role": "assistant",
        "content": full_response,
        "timestamp": datetime.now().strftime("%I:%M %p"),
        "response_time": f"{response_time:.2f}"
    }
    st.session_state.messages.append(bot_msg)
    
    # Remove typing indicator
    typing_placeholder.empty()
    
    st.rerun()

# Clear chat button
col1, col2, col3 = st.columns([1, 1, 3])
with col1:
    if st.button("🗑️ Clear Chat", key="clear_btn", use_container_width=True):
        st.session_state.messages = []
        st.session_state.response_times = []
        st.session_state.start_time = time.time()
        st.rerun()

with col2:
    if st.button("📥 Export", key="export_btn", use_container_width=True):
        if len(st.session_state.messages) > 0:
            chat_text = "\n\n".join([f"{'You' if m['role'] == 'user' else 'Assistant'}: {m['content']}" for m in st.session_state.messages])
            st.download_button(
                label="Download Chat",
                data=chat_text,
                file_name=f"dexwin_chat_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                mime="text/plain"
            )

# Enhanced footer
st.markdown("""
<div class="footer">
    <p>🚀 Powered by <strong>Claude Haiku</strong> × <strong>Streamlit</strong></p>
    <p style="margin-top: 8px; color: #64748b; font-size: 0.9em;">
        <a href="https://dexwin.net" style="color: #3b82f6;">Visit Dexwin.net</a> • 
        <a href="https://dexwin.net/gh/about" style="color: #3b82f6;">About Us</a> • 
        <a href="https://dexwin.net/gh/services" style="color: #3b82f6;">Services</a>
    </p>
</div>
""", unsafe_allow_html=True)