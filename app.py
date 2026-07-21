import inspect

import streamlit as st
from groq import Groq

# ---------------------------
# Page Config
# ---------------------------
st.set_page_config(
    page_title="AI Chatbot",
    page_icon="🤖",
    layout="centered"
)

# ---------------------------
# Theme State
# ---------------------------
if "theme" not in st.session_state:
    st.session_state.theme = "dark"

THEMES = {
    "dark": {
        "app_bg": "linear-gradient(-45deg, #0f0c29, #302b63, #24243e, #1a1a2e)",
        "orb": "radial-gradient(circle, rgba(99,102,241,0.15) 0%, transparent 70%)",
        "title_gradient": "linear-gradient(90deg, #a78bfa, #60a5fa, #34d399)",
        "subtitle": "rgba(255,255,255,0.55)",
        "card_bg": "rgba(255,255,255,0.06)",
        "card_border": "rgba(255,255,255,0.1)",
        "card_title": "#e2e8f0",
        "card_text": "rgba(255,255,255,0.45)",
        "chip_bg": "rgba(99,102,241,0.15)",
        "chip_border": "rgba(99,102,241,0.3)",
        "chip_text": "#a5b4fc",
        "chip_hover": "rgba(99,102,241,0.3)",
        "message_bg": "rgba(255,255,255,0.07)",
        "message_border": "rgba(255,255,255,0.1)",
        "message_shadow": "0 4px 20px rgba(0,0,0,0.2)",
        "message_text": "#e2e8f0",
        "input_bar_bg": "rgba(15, 12, 41, 0.6)",
        "input_bar_border": "rgba(255,255,255,0.08)",
        "input_bg": "rgba(255,255,255,0.08)",
        "input_border": "rgba(255,255,255,0.15)",
        "input_text": "#e2e8f0",
        "input_placeholder": "rgba(255,255,255,0.35)",
        "input_focus_shadow": "0 0 0 3px rgba(99,102,241,0.2)",
        "cursor": "#60a5fa",
        "typing_dot": "#60a5fa",
        "scrollbar": "rgba(99,102,241,0.4)",
        "toggle_bg": "rgba(255,255,255,0.08)",
        "toggle_border": "rgba(255,255,255,0.12)",
        "toggle_active_bg": "rgba(99,102,241,0.35)",
        "toggle_active_text": "#ffffff",
        "toggle_inactive_text": "rgba(255,255,255,0.5)",
    },
    "light": {
        "app_bg": "linear-gradient(-45deg, #e0e7ff, #f0f9ff, #ecfdf5, #faf5ff)",
        "orb": "radial-gradient(circle, rgba(99,102,241,0.12) 0%, transparent 70%)",
        "title_gradient": "linear-gradient(90deg, #4f46e5, #2563eb, #059669)",
        "subtitle": "#64748b",
        "card_bg": "rgba(255,255,255,0.85)",
        "card_border": "rgba(99,102,241,0.15)",
        "card_title": "#1e293b",
        "card_text": "#64748b",
        "chip_bg": "rgba(99,102,241,0.08)",
        "chip_border": "rgba(99,102,241,0.2)",
        "chip_text": "#4f46e5",
        "chip_hover": "rgba(99,102,241,0.18)",
        "message_bg": "rgba(255,255,255,0.92)",
        "message_border": "rgba(148,163,184,0.25)",
        "message_shadow": "0 4px 16px rgba(99,102,241,0.08)",
        "message_text": "#1e293b",
        "input_bar_bg": "rgba(255,255,255,0.85)",
        "input_bar_border": "rgba(148,163,184,0.2)",
        "input_bg": "#ffffff",
        "input_border": "rgba(148,163,184,0.35)",
        "input_text": "#1e293b",
        "input_placeholder": "#94a3b8",
        "input_focus_shadow": "0 0 0 3px rgba(99,102,241,0.15)",
        "cursor": "#2563eb",
        "typing_dot": "#6366f1",
        "scrollbar": "rgba(99,102,241,0.3)",
        "toggle_bg": "rgba(255,255,255,0.9)",
        "toggle_border": "rgba(148,163,184,0.3)",
        "toggle_active_bg": "#6366f1",
        "toggle_active_text": "#ffffff",
        "toggle_inactive_text": "#64748b",
    },
}

t = THEMES[st.session_state.theme]

# ---------------------------
# Custom CSS & Animations
# ---------------------------
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

.stApp {{
    background: {t["app_bg"]};
    background-size: 400% 400%;
    animation: gradientShift 12s ease infinite;
    font-family: 'Inter', sans-serif;
    transition: background 0.4s ease;
}}

@keyframes gradientShift {{
    0%   {{ background-position: 0% 50%; }}
    50%  {{ background-position: 100% 50%; }}
    100% {{ background-position: 0% 50%; }}
}}

.stApp::before {{
    content: '';
    position: fixed;
    top: -10%;
    right: -5%;
    width: 400px;
    height: 400px;
    background: {t["orb"]};
    border-radius: 50%;
    animation: floatOrb 8s ease-in-out infinite;
    pointer-events: none;
    z-index: 0;
}}

@keyframes floatOrb {{
    0%, 100% {{ transform: translate(0, 0) scale(1); }}
    50%      {{ transform: translate(-30px, 40px) scale(1.1); }}
}}

.header-wrap {{
    text-align: center;
    padding: 28px 0 12px;
    animation: fadeSlideDown 0.7s ease-out;
}}

@keyframes fadeSlideDown {{
    from {{ opacity: 0; transform: translateY(-20px); }}
    to   {{ opacity: 1; transform: translateY(0); }}
}}

.bot-icon {{
    font-size: 52px;
    display: inline-block;
    animation: pulse 2.5s ease-in-out infinite;
}}

@keyframes pulse {{
    0%, 100% {{ transform: scale(1); }}
    50%      {{ transform: scale(1.12); }}
}}

.main-title {{
    font-size: 38px;
    font-weight: 700;
    margin: 8px 0 4px;
    letter-spacing: -0.5px;
    background: {t["title_gradient"]};
    background-size: 200% auto;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    animation: shimmer 4s linear infinite;
}}

@keyframes shimmer {{
    0%   {{ background-position: 0% center; }}
    100% {{ background-position: 200% center; }}
}}

.subtitle {{
    color: {t["subtitle"]};
    font-size: 15px;
    margin-bottom: 0;
    font-weight: 400;
}}

.status-badge {{
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: rgba(52, 211, 153, 0.12);
    border: 1px solid rgba(52, 211, 153, 0.3);
    color: #34d399;
    font-size: 12px;
    font-weight: 600;
    padding: 4px 12px;
    border-radius: 20px;
    margin-top: 10px;
    animation: fadeIn 1s ease 0.5s both;
}}

.status-dot {{
    width: 7px;
    height: 7px;
    background: #34d399;
    border-radius: 50%;
    animation: blink 1.5s ease-in-out infinite;
}}

@keyframes blink {{
    0%, 100% {{ opacity: 1; }}
    50%      {{ opacity: 0.3; }}
}}

@keyframes fadeIn {{
    from {{ opacity: 0; }}
    to   {{ opacity: 1; }}
}}

.welcome-card {{
    background: {t["card_bg"]};
    backdrop-filter: blur(12px);
    border: 1px solid {t["card_border"]};
    border-radius: 20px;
    padding: 32px 28px;
    text-align: center;
    margin: 20px 0 10px;
    animation: fadeSlideUp 0.8s ease-out 0.3s both;
    transition: background 0.4s ease, border-color 0.4s ease;
}}

@keyframes fadeSlideUp {{
    from {{ opacity: 0; transform: translateY(24px); }}
    to   {{ opacity: 1; transform: translateY(0); }}
}}

.welcome-card h3 {{
    color: {t["card_title"]};
    font-size: 20px;
    font-weight: 600;
    margin: 0 0 8px;
}}

.welcome-card p {{
    color: {t["card_text"]};
    font-size: 14px;
    margin: 0 0 20px;
}}

.suggestion-chips {{
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    justify-content: center;
}}

.chip {{
    background: {t["chip_bg"]};
    border: 1px solid {t["chip_border"]};
    color: {t["chip_text"]};
    font-size: 13px;
    padding: 6px 14px;
    border-radius: 20px;
    cursor: default;
    transition: all 0.25s ease;
}}

.chip:hover {{
    background: {t["chip_hover"]};
    transform: translateY(-2px);
}}

div[data-testid="stChatMessage"] {{
    background: {t["message_bg"]} !important;
    backdrop-filter: blur(10px);
    border: 1px solid {t["message_border"]} !important;
    border-radius: 18px !important;
    padding: 14px 18px !important;
    margin-bottom: 14px !important;
    box-shadow: {t["message_shadow"]} !important;
    animation: messageIn 0.4s ease-out both;
    color: {t["message_text"]} !important;
    transition: background 0.4s ease, border-color 0.4s ease, box-shadow 0.4s ease;
}}

@keyframes messageIn {{
    from {{ opacity: 0; transform: translateY(12px) scale(0.97); }}
    to   {{ opacity: 1; transform: translateY(0) scale(1); }}
}}

div[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) {{
    border-left: 3px solid #6366f1 !important;
}}

div[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"]) {{
    border-left: 3px solid #34d399 !important;
}}

div[data-testid="stChatMessage"] p,
div[data-testid="stChatMessage"] li,
div[data-testid="stChatMessage"] span {{
    color: {t["message_text"]} !important;
}}

.cursor-blink {{
    display: inline-block;
    width: 2px;
    height: 1em;
    background: {t["cursor"]};
    margin-left: 2px;
    vertical-align: text-bottom;
    animation: cursorBlink 0.8s step-end infinite;
}}

@keyframes cursorBlink {{
    0%, 100% {{ opacity: 1; }}
    50%      {{ opacity: 0; }}
}}

.stChatInputContainer {{
    background: {t["input_bar_bg"]} !important;
    backdrop-filter: blur(16px);
    border-top: 1px solid {t["input_bar_border"]} !important;
    padding: 12px 0 !important;
    transition: background 0.4s ease;
}}

.stChatInputContainer textarea {{
    background: {t["input_bg"]} !important;
    border: 1px solid {t["input_border"]} !important;
    border-radius: 14px !important;
    color: {t["input_text"]} !important;
    font-family: 'Inter', sans-serif !important;
    transition: border-color 0.3s ease, box-shadow 0.3s ease, background 0.4s ease !important;
}}

.stChatInputContainer textarea:focus {{
    border-color: #6366f1 !important;
    box-shadow: {t["input_focus_shadow"]} !important;
}}

.stChatInputContainer textarea::placeholder {{
    color: {t["input_placeholder"]} !important;
}}

/* Toolbar buttons (theme + clear) */
div[data-testid="column"]:has(.theme-btn) .stButton > button,
div[data-testid="column"]:has(.clear-btn) .stButton > button {{
    border-radius: 12px !important;
    padding: 8px 14px !important;
    font-weight: 600 !important;
    font-size: 16px !important;
    transition: all 0.25s ease !important;
    min-height: 42px !important;
}}

.theme-btn .stButton > button {{
    background: {t["toggle_bg"]} !important;
    color: {t["toggle_inactive_text"]} !important;
    border: 1px solid {t["toggle_border"]} !important;
}}

.theme-btn .stButton > button:hover {{
    background: {t["chip_hover"]} !important;
    color: {t["chip_text"]} !important;
    transform: scale(1.04) !important;
}}

.theme-btn-active .stButton > button {{
    background: {t["toggle_active_bg"]} !important;
    color: {t["toggle_active_text"]} !important;
    border: 1px solid {t["toggle_active_bg"]} !important;
    box-shadow: 0 4px 14px rgba(99,102,241,0.25) !important;
}}

.clear-btn .stButton > button {{
    background: rgba(239, 68, 68, 0.12) !important;
    color: #ef4444 !important;
    border: 1px solid rgba(239, 68, 68, 0.25) !important;
}}

.clear-btn .stButton > button:hover {{
    background: rgba(239, 68, 68, 0.25) !important;
    color: #fff !important;
    transform: scale(1.05) !important;
    box-shadow: 0 4px 15px rgba(239, 68, 68, 0.25) !important;
}}

.typing-indicator {{
    display: flex;
    align-items: center;
    gap: 5px;
    padding: 4px 0;
}}

.typing-indicator span {{
    width: 8px;
    height: 8px;
    background: {t["typing_dot"]};
    border-radius: 50%;
    animation: typingBounce 1.2s ease-in-out infinite;
}}

.typing-indicator span:nth-child(2) {{ animation-delay: 0.2s; }}
.typing-indicator span:nth-child(3) {{ animation-delay: 0.4s; }}

@keyframes typingBounce {{
    0%, 60%, 100% {{ transform: translateY(0); opacity: 0.4; }}
    30%           {{ transform: translateY(-8px); opacity: 1; }}
}}

::-webkit-scrollbar {{ width: 6px; }}
::-webkit-scrollbar-track {{ background: transparent; }}
::-webkit-scrollbar-thumb {{
    background: {t["scrollbar"]};
    border-radius: 3px;
}}

footer, header, #MainMenu {{ visibility: hidden; }}

.block-container {{
    padding-top: 1rem !important;
    max-width: 760px !important;
}}

.toolbar-label {{
    color: {t["subtitle"]};
    font-size: 12px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    margin-bottom: 6px;
}}

.voice-panel {{
    background: {t["card_bg"]};
    border: 1px solid {t["card_border"]};
    border-radius: 16px;
    padding: 14px 18px;
    margin: 8px 0 4px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 12px;
    animation: fadeSlideUp 0.5s ease-out both;
}}

.voice-panel-text {{
    color: {t["card_text"]};
    font-size: 13px;
    margin: 0;
}}

.voice-panel-text strong {{
    color: {t["card_title"]};
}}

.voice-status {{
    color: {t["chip_text"]};
    font-size: 12px;
    font-weight: 600;
    margin-top: 6px;
    min-height: 18px;
}}

.mic-recording {{
    animation: micPulse 1.2s ease-in-out infinite;
}}

@keyframes micPulse {{
    0%, 100% {{ box-shadow: 0 0 0 0 rgba(239, 68, 68, 0.45); }}
    50%      {{ box-shadow: 0 0 0 10px rgba(239, 68, 68, 0); }}
}}
</style>
""", unsafe_allow_html=True)

# ---------------------------
# Initialize Groq Client
# ---------------------------
# def get_groq_api_key():
#     if "GROQ_API_KEY" in st.secrets:
#         return st.secrets["GROQ_API_KEY"]
#     if os.path.exists("groq.txt"):
#         with open("groq.txt", encoding="utf-8") as f:
#             return f.read().strip()
#     st.error("Add GROQ_API_KEY to `.streamlit/secrets.toml` or put your key in `groq.txt`.")
#     st.stop()


client = Groq(api_key=st.secrets["GROQ_API_KEY"])


# ---------------------------
# Helpers
# ---------------------------
_SUPPORTS_AUDIO = "accept_audio" in inspect.signature(st.chat_input).parameters


def transcribe_audio(audio_file):
    audio_bytes = audio_file.getvalue()
    transcription = client.audio.transcriptions.create(
        model="whisper-large-v3-turbo",
        file=("recording.wav", audio_bytes, "audio/wav"),
        language="en",
    )
    return transcription.text.strip()


def extract_prompt_text(prompt):
    if prompt is None:
        return None, False, None

    if hasattr(prompt, "text") and prompt.text and prompt.text.strip():
        return prompt.text.strip(), False, getattr(prompt, "audio", None)

    if hasattr(prompt, "audio") and prompt.audio:
        return None, True, prompt.audio

    if isinstance(prompt, str) and prompt.strip():
        return prompt.strip(), False, None

    return None, False, None


def run_chat_turn(user_text, from_voice=False, audio_file=None):
    display_text = user_text
    if from_voice:
        display_text = f"🎤 {user_text}"

    st.session_state.messages.append({"role": "user", "content": user_text})

    with st.chat_message("user"):
        st.markdown(display_text)
        if from_voice and audio_file is not None:
            st.audio(audio_file, format="audio/wav")

    with st.chat_message("assistant"):
        placeholder = st.empty()
        placeholder.markdown(
            '<div class="typing-indicator"><span></span><span></span><span></span></div>',
            unsafe_allow_html=True,
        )

        response = ""
        first_token = True

        completion = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=st.session_state.messages,
            stream=True,
        )

        for chunk in completion:
            if chunk.choices[0].delta.content:
                if first_token:
                    first_token = False
                response += chunk.choices[0].delta.content
                placeholder.markdown(
                    response + '<span class="cursor-blink"></span>',
                    unsafe_allow_html=True,
                )

        placeholder.markdown(response)

    st.session_state.messages.append({"role": "assistant", "content": response})

# ---------------------------
# Session State
# ---------------------------
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "system",
            "content": "You are a helpful AI assistant."
        }
    ]

# ---------------------------
# Toolbar: Theme toggle + Clear chat
# ---------------------------
tool_left, tool_mid, tool_right = st.columns([2.2, 4.6, 1.2])

with tool_left:
    st.markdown('<p class="toolbar-label">Theme</p>', unsafe_allow_html=True)
    theme_dark_col, theme_light_col = st.columns(2)

    with theme_dark_col:
        if st.button(
            "🌙 Dark",
            key="theme_dark",
            use_container_width=True,
            type="primary" if st.session_state.theme == "dark" else "secondary",
        ):
            if st.session_state.theme != "dark":
                st.session_state.theme = "dark"
                st.rerun()

    with theme_light_col:
        if st.button(
            "☀️ Light",
            key="theme_light",
            use_container_width=True,
            type="primary" if st.session_state.theme == "light" else "secondary",
        ):
            if st.session_state.theme != "light":
                st.session_state.theme = "light"
                st.rerun()

with tool_right:
    st.markdown('<p class="toolbar-label">&nbsp;</p>', unsafe_allow_html=True)
    if st.button("🗑️", key="clear_chat", use_container_width=True, help="Clear chat", type="secondary"):
        st.session_state.messages = [
            {
                "role": "system",
                "content": "You are a helpful AI assistant."
            }
        ]
        st.rerun()

# ---------------------------
# Header
# ---------------------------
st.markdown("""
<div class="header-wrap">
    <div class="bot-icon">🤖</div>
    <h1 class="main-title">AI Chatbot</h1>
    <p class="subtitle">Powered by Groq · GPT-OSS-120B</p>
    <div class="status-badge">
        <span class="status-dot"></span> Online
    </div>
</div>
""", unsafe_allow_html=True)

# ---------------------------
# Welcome card (shown when no user messages yet)
# ---------------------------
user_messages = [m for m in st.session_state.messages if m["role"] != "system"]

if not user_messages:
    st.markdown("""
    <div class="welcome-card">
        <h3>👋 Hello! How can I help you today?</h3>
        <p>Ask me anything — coding, writing, ideas, or general questions.</p>
        <div class="suggestion-chips">
            <span class="chip">💡 Explain a concept</span>
            <span class="chip">✍️ Help me write</span>
            <span class="chip">🐍 Debug my code</span>
            <span class="chip">🌍 Fun facts</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ---------------------------
# Display Chat
# ---------------------------
for message in st.session_state.messages:

    if message["role"] == "system":
        continue

    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ---------------------------
# Voice input hint
# ---------------------------
if _SUPPORTS_AUDIO:
    st.markdown("""
    <div class="voice-panel">
        <p class="voice-panel-text">
            <strong>🎤 Microphone enabled</strong> — tap the mic icon in the chat box below,
            allow browser access, record your message, then send.
        </p>
    </div>
    """, unsafe_allow_html=True)
else:
    st.info("Install Streamlit 1.52+ for microphone support: `pip install -U streamlit`")

# ---------------------------
# Chat Input
# ---------------------------
if _SUPPORTS_AUDIO:
    prompt = st.chat_input(
        "Type or tap the mic to speak...",
        accept_audio=True,
        key="chat_input",
    )
else:
    prompt = st.chat_input("Ask me anything...", key="chat_input")

user_text, from_voice, audio_file = extract_prompt_text(prompt)

if user_text:
    run_chat_turn(user_text)
elif from_voice and audio_file is not None:
    with st.spinner("Transcribing your voice..."):
        try:
            transcribed = transcribe_audio(audio_file)
        except Exception as exc:
            st.error(f"Could not transcribe audio: {exc}")
            st.stop()

    if not transcribed:
        st.warning("No speech detected. Please try again.")
    else:
        run_chat_turn(transcribed, from_voice=True, audio_file=audio_file)

