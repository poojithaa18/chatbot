import streamlit as st
from groq import Groq

# ---------------------------
# Page Config
# ---------------------------
st.set_page_config(
    page_title="Pooji conversational chatbot",
    page_icon="🤖",
    layout="centered"
)

# ---------------------------
# Custom CSS
# ---------------------------
st.markdown("""
<style>
.stApp {
    background-color: white !important;
}

html, body, [class*="css"], [data-testid="stAppViewContainer"] {
    color: black !important;
}

[data-testid="stChatInput"] textarea {
    color: black !important;
    background: white !important;
}

[data-testid="stMarkdownContainer"] {
    color: black !important;
}
</style>
""", unsafe_allow_html=True)

# ---------------------------
# Initialize Groq Client
# ---------------------------
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

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
# Header
# ---------------------------
st.markdown("<h1 class='main-title'>🤖 Pooji conversational chatbot</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Powered by Groq GPT-OSS-120B</p>", unsafe_allow_html=True)

# ---------------------------
# Clear Chat Button
# ---------------------------
col1, col2 = st.columns([6,1])

with col2:
    if st.button("🗑️"):
        st.session_state.messages = [
            {
                "role":"system",
                "content":"You are a helpful AI assistant."
            }
        ]
        st.rerun()

# ---------------------------
# Display Chat
# ---------------------------
for message in st.session_state.messages:

    if message["role"] == "system":
        continue

    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ---------------------------
# Chat Input
# ---------------------------
prompt = st.chat_input("Ask me anything...")

if prompt:

    st.session_state.messages.append(
        {
            "role":"user",
            "content":prompt
        }
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):

        placeholder = st.empty()

        response = ""

        completion = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=st.session_state.messages,
            stream=True
        )

        for chunk in completion:

            if chunk.choices[0].delta.content:

                response += chunk.choices[0].delta.content

                placeholder.markdown(response + "▌")

        placeholder.markdown(response)

    st.session_state.messages.append(
        {
            "role":"assistant",
            "content":response
        }
    )
