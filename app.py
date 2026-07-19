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
    background: linear-gradient(-45deg,#ffffff,#f8fafc,#eef6ff,#ffffff);
    background-size:400% 400%;
    animation: gradientBG 12s ease infinite;
}

@keyframes gradientBG{
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
   Black Font
=========================== */

html,
body,
[class*="css"],
[data-testid="stAppViewContainer"],
[data-testid="stMarkdownContainer"],
label,
span,
p,
h1,
h2,
h3,
h4,
h5,
h6{
    color:#000 !important;
}


/* ===========================
   Chat Messages
=========================== */

div[data-testid="stChatMessage"]{

    background:white;

    border-radius:18px;

    padding:15px;

    margin-bottom:15px;

    border:1px solid #E5E7EB;

    box-shadow:0px 6px 18px rgba(0,0,0,.08);

    animation:slideUp .4s ease;
}


@keyframes slideUp{

    from{
        opacity:0;
        transform:translateY(25px);
    }

    to{
        opacity:1;
        transform:translateY(0);
    }

}


/* Hover Animation */

div[data-testid="stChatMessage"]:hover{

    transform:translateY(-4px);

    transition:.3s;

    box-shadow:0 12px 25px rgba(0,0,0,.12);

}


/* ===========================
   Chat Input
=========================== */

[data-testid="stChatInput"]{

    border-radius:20px;

    border:2px solid #D1D5DB;

    background:white;

    box-shadow:0 4px 12px rgba(0,0,0,.08);

    transition:.3s;

}


[data-testid="stChatInput"]:focus-within{

    border-color:#2563EB;

    box-shadow:0 0 15px rgba(37,99,235,.25);

}


[data-testid="stChatInput"] textarea{

    color:black !important;

    background:white !important;

}


/* ===========================
   Buttons
=========================== */

.stButton>button{

    background:#2563EB;

    color:white;

    border-radius:12px;

    border:none;

    transition:.3s;

    font-weight:600;

}


.stButton>button:hover{

    transform:scale(1.05);

    background:#1D4ED8;

}


/* ===========================
   Scrollbar
=========================== */

::-webkit-scrollbar{

    width:8px;

}

::-webkit-scrollbar-thumb{

    background:#BFC5D2;

    border-radius:10px;

}

::-webkit-scrollbar-thumb:hover{

    background:#94A3B8;

}


/* ===========================
   Hide Streamlit Branding
=========================== */

#MainMenu{
    visibility:hidden;
}

header{
    visibility:hidden;
}

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
