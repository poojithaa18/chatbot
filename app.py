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

/* ---------- Animated Background ---------- */

.stApp{
    background: linear-gradient(-45deg,#ffffff,#f5f7fa,#eef4ff,#ffffff);
    background-size:400% 400%;
    animation:bgAnimation 12s ease infinite;
}

/* Background Animation */
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

/* ---------- Global Font ---------- */

html,
body,
[class*="css"],
[data-testid="stAppViewContainer"]{
    color:black !important;
    font-family:"Segoe UI",sans-serif;
}

/* ---------- Title Animation ---------- */

.main-title{
    color:black;
    text-align:center;
    font-size:42px;
    font-weight:700;
    animation:slideDown 1s ease;
}

.subtitle{
    color:#555;
    text-align:center;
    animation:fadeIn 2s ease;
}

@keyframes slideDown{
    from{
        opacity:0;
        transform:translateY(-40px);
    }
    to{
        opacity:1;
        transform:translateY(0);
    }
}

@keyframes fadeIn{
    from{
        opacity:0;
    }
    to{
        opacity:1;
    }
}

/* ---------- Chat Messages ---------- */

div[data-testid="stChatMessage"]{

    background:white;
    border-radius:18px;
    padding:15px;
    margin:10px 0;

    border:1px solid #E5E7EB;

    box-shadow:0 5px 20px rgba(0,0,0,.08);

    animation:messageAnimation .4s ease;

    transition:.3s;
}

div[data-testid="stChatMessage"]:hover{

    transform:translateY(-3px);

    box-shadow:0 12px 25px rgba(0,0,0,.15);

}

/* Message Animation */

@keyframes messageAnimation{

    from{
        opacity:0;
        transform:translateY(20px);
    }

    to{
        opacity:1;
        transform:translateY(0);
    }

}

/* ---------- Chat Input ---------- */

[data-testid="stChatInput"]{

    animation:fadeInUp .8s ease;

}

[data-testid="stChatInput"] textarea{

    background:white !important;

    color:black !important;

    border-radius:15px !important;

    border:2px solid #d1d5db !important;

}

[data-testid="stChatInput"] textarea:focus{

    border:2px solid #4F46E5 !important;

    box-shadow:0 0 10px rgba(79,70,229,.25);

}

/* ---------- Buttons ---------- */

.stButton>button{

    background:#4F46E5;

    color:white;

    border:none;

    border-radius:10px;

    transition:.3s;

}

.stButton>button:hover{

    background:#4338CA;

    transform:scale(1.05);

}

/* ---------- Fade Up ---------- */

@keyframes fadeInUp{

    from{

        opacity:0;

        transform:translateY(25px);

    }

    to{

        opacity:1;

        transform:translateY(0);

    }

}

/* ---------- Markdown ---------- */

[data-testid="stMarkdownContainer"]{

    color:black !important;

}

/* ---------- Hide Streamlit ---------- */

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
