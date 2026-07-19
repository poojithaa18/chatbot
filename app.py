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

/* ===========================
   Animated Background
=========================== */

.stApp{
    background: linear-gradient(-45deg,
    #ffffff,
    #edf4ff,
    #f8f4ff,
    #ffffff);
    background-size:400% 400%;
    animation:bgAnimation 12s ease infinite;
    overflow:hidden;
}

/* Moving Gradient */

@keyframes bgAnimation{

0%{
background-position:0% 50%;
}

50%{
background-position:100% 50%;
}

100%{
background-position:0% 50%;
}

}


/* ===========================
Floating Neon Blobs
=========================== */

.stApp::before{

content:"";

position:fixed;

width:320px;

height:320px;

background:#7c3aed;

top:-120px;

left:-120px;

border-radius:50%;

filter:blur(90px);

opacity:.35;

animation:blob1 9s ease-in-out infinite;

z-index:-1;

}

.stApp::after{

content:"";

position:fixed;

width:350px;

height:350px;

background:#0ea5e9;

bottom:-120px;

right:-120px;

border-radius:50%;

filter:blur(100px);

opacity:.35;

animation:blob2 10s ease-in-out infinite;

z-index:-1;

}

@keyframes blob1{

0%,100%{
transform:translate(0,0);
}

50%{
transform:translate(90px,70px);
}

}

@keyframes blob2{

0%,100%{
transform:translate(0,0);
}

50%{
transform:translate(-100px,-80px);
}

}


/* ===========================
Black Font
=========================== */

html,
body,
p,
span,
label,
h1,
h2,
h3,
h4,
h5,
h6,
textarea{

color:#000 !important;

}


/* ===========================
Title
=========================== */

.main-title{

text-align:center;

font-size:44px;

font-weight:700;

color:#111827;

animation:title 1.2s ease;

}

@keyframes title{

0%{

opacity:0;

transform:translateY(-40px);

}

100%{

opacity:1;

transform:translateY(0);

}

}


/* ===========================
Chat Bubble
=========================== */

div[data-testid="stChatMessage"]{

background:rgba(255,255,255,.65);

backdrop-filter:blur(20px);

border-radius:24px;

padding:18px;

margin-bottom:15px;

border:1px solid rgba(255,255,255,.7);

box-shadow:

0 10px 35px rgba(124,58,237,.15);

transition:.4s;

animation:message .5s ease;

}

div[data-testid="stChatMessage"]:hover{

transform:translateY(-4px);

box-shadow:

0 18px 40px rgba(14,165,233,.25);

}


/* ===========================
Message Animation
=========================== */

@keyframes message{

0%{

opacity:0;

transform:translateY(25px);

}

100%{

opacity:1;

transform:translateY(0);

}

}


/* ===========================
Chat Input
=========================== */

[data-testid="stChatInput"]{

background:white;

border-radius:35px;

border:2px solid #d8b4fe;

box-shadow:

0 10px 30px rgba(124,58,237,.18);

transition:.3s;

}

[data-testid="stChatInput"]:focus-within{

border-color:#7c3aed;

box-shadow:

0 0 25px rgba(124,58,237,.45);

transform:scale(1.01);

}

[data-testid="stChatInput"] textarea{

color:black !important;

background:transparent !important;

font-size:17px;

}


/* ===========================
Buttons
=========================== */

.stButton>button{

background:linear-gradient(90deg,#7c3aed,#2563eb);

color:white;

border:none;

border-radius:30px;

font-weight:600;

padding:10px 20px;

transition:.35s;

}

.stButton>button:hover{

transform:scale(1.08);

box-shadow:

0 0 25px rgba(124,58,237,.45);

}


/* ===========================
Scrollbar
=========================== */

::-webkit-scrollbar{

width:8px;

}

::-webkit-scrollbar-thumb{

background:linear-gradient(#7c3aed,#0ea5e9);

border-radius:10px;

}


/* ===========================
Hide Streamlit
=========================== */

header{

visibility:hidden;

}

footer{

visibility:hidden;

}

#MainMenu{

visibility:hidden;

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
