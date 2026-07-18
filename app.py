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

/* Main App */
.stApp{
    background: #F8F9FA;
}

/* Title */
.main-title{
    text-align: center;
    color: #2563EB;
    font-size: 42px;
    font-weight: 700;
}

/* Subtitle */
.subtitle{
    text-align: center;
    color: #6B7280;
    font-size: 18px;
    margin-bottom: 25px;
}

/* Chat Messages */
div[data-testid="stChatMessage"]{
    background: white;
    border: 1px solid #E5E7EB;
    border-radius: 16px;
    padding: 12px;
    margin-bottom: 12px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.08);
}

/* Chat Input */
.stChatInputContainer{
    background: white;
    border-top: 1px solid #E5E7EB;
}

/* Buttons */
.stButton>button{
    background-color: #2563EB;
    color: white;
    border: none;
    border-radius: 10px;
    padding: 8px 18px;
    font-weight: 600;
}

.stButton>button:hover{
    background-color: #1D4ED8;
    color: white;
}

/* Hide Streamlit Branding */
footer{
    visibility: hidden;
}

header{
    visibility: hidden;
}

#MainMenu{
    visibility: hidden;
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
