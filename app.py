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

/* --------------------------------------------------
   Animated Background
-------------------------------------------------- */

.stApp{
    background: linear-gradient(-45deg,
        #ffffff,
        #f3f8ff,
        #eef7ff,
        #ffffff);
    background-size:400% 400%;
    animation: gradientBG 15s ease infinite;
    overflow:hidden;
}

@keyframes gradientBG{
    0%{background-position:0% 50%;}
    50%{background-position:100% 50%;}
    100%{background-position:0% 50%;}
}

/* --------------------------------------------------
   Floating Glow Circles
-------------------------------------------------- */

.stApp::before,
.stApp::after{
    content:"";
    position:fixed;
    border-radius:50%;
    filter:blur(80px);
    z-index:-1;
}

.stApp::before{
    width:280px;
    height:280px;
    background:#7dd3fc;
    top:-80px;
    left:-80px;
    animation:float1 8s ease-in-out infinite;
}

.stApp::after{
    width:320px;
    height:320px;
    background:#c4b5fd;
    bottom:-120px;
    right:-120px;
    animation:float2 10s ease-in-out infinite;
}

@keyframes float1{
    0%,100%{transform:translateY(0);}
    50%{transform:translateY(50px);}
}

@keyframes float2{
    0%,100%{transform:translateY(0);}
    50%{transform:translateY(-60px);}
}

/* --------------------------------------------------
   Black Font Everywhere
-------------------------------------------------- */

html,
body,
p,
span,
label,
h1,h2,h3,h4,h5,h6,
[data-testid="stMarkdownContainer"]{
    color:#000 !important;
}

/* --------------------------------------------------
   Title Animation
-------------------------------------------------- */

.main-title{
    text-align:center;
    color:#000;
    font-size:46px;
    font-weight:700;
    animation:fadeDown 1s ease;
}

@keyframes fadeDown{
    from{
        opacity:0;
        transform:translateY(-40px);
    }
    to{
        opacity:1;
        transform:translateY(0);
    }
}

/* --------------------------------------------------
   Chat Messages
-------------------------------------------------- */

div[data-testid="stChatMessage"]{

    background:white;
    border-radius:18px;
    border:1px solid #e5e7eb;

    padding:15px;

    margin-bottom:14px;

    box-shadow:0 6px 20px rgba(0,0,0,.08);

    transition:.35s;
}

div[data-testid="stChatMessage"]:hover{

    transform:translateY(-3px);

    box-shadow:0 12px 30px rgba(0,0,0,.15);

}

/* --------------------------------------------------
   Chat Input
-------------------------------------------------- */

[data-testid="stChatInput"]{

    border-radius:30px;

    border:2px solid #dbeafe;

    box-shadow:0 6px 20px rgba(0,0,0,.08);

    transition:.3s;

}

[data-testid="stChatInput"]:focus-within{

    border-color:#2563eb;

    box-shadow:0 0 18px rgba(37,99,235,.35);

}

/* Textarea */

[data-testid="stChatInput"] textarea{

    color:#000 !important;

    background:white !important;

}

/* --------------------------------------------------
   Send Button Animation
-------------------------------------------------- */

.stButton>button{

    background:#2563eb;

    color:white;

    border:none;

    border-radius:30px;

    transition:.3s;

    font-weight:bold;

}

.stButton>button:hover{

    transform:scale(1.06);

    background:#1d4ed8;

    box-shadow:0 0 18px rgba(37,99,235,.45);

}

/* --------------------------------------------------
   Scrollbar
-------------------------------------------------- */

::-webkit-scrollbar{
    width:8px;
}

::-webkit-scrollbar-thumb{
    background:#60a5fa;
    border-radius:10px;
}

::-webkit-scrollbar-track{
    background:#f3f4f6;
}

/* --------------------------------------------------
   Fade Animation for Messages
-------------------------------------------------- */

div[data-testid="stChatMessage"]{

    animation:fadeIn .45s ease;

}

@keyframes fadeIn{

    from{

        opacity:0;

        transform:translateY(18px);

    }

    to{

        opacity:1;

        transform:translateY(0);

    }

}

/* --------------------------------------------------
   Hide Streamlit Branding
-------------------------------------------------- */

#MainMenu,
header,
footer{

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
