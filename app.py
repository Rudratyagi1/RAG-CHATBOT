#basic imports 
import asyncio
import nest_asyncio
import os
import streamlit as st
from dotenv import load_dotenv
from pathlib import Path


#import custom modules
from src.loader import load_documents
from src.splitter import split_documents
#from src.embedder import create_embeddings
from src.vectorstore import build_vectorstore
from src.rag_chain import build_rag_chain
from src.followup import build_history_aware_chain


# Setup asyncio event loop to avoid runtime errors
asyncio.set_event_loop(asyncio.new_event_loop())
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
nest_asyncio.apply(loop)


# Load api key
load_dotenv()
google_api_key = os.getenv("GOOGLE_API_KEY")
print("GOOGLE_API_KEY:", google_api_key)


# Page config
st.set_page_config(page_title="DevOps RAG Chatbot", layout="wide",  page_icon="🤖" , initial_sidebar_state="expanded")


# Centered title with avatar using HTML in Streamlit
avatar_url = "https://avatars.githubusercontent.com/u/87880186?v=4" 
st.markdown(f"""
<div style="display: flex; justify-content: center; align-items: center; gap: 10px; margin-bottom: 20px;">
    <img src="{avatar_url}" alt="avatar" width="50" height="50" style="border-radius: 50%;">
    <h1 style="margin: 0; text-align: center;">DevOps RAG Chatbot</h1>
</div>
""", unsafe_allow_html=True)


# Custom CSS for wide inputs, rounded bubbles, and scrolling history
st.markdown("""
<style>
/* Make chat input wide and rounded */
div[role="textbox"] {
    border-radius: 12px !important;
    padding: 10px !important;
    max-width: 800px !important;
    margin: auto;
    font-size: 16px;
}

/* Scrollable chat container with max height */
main .block-container {
    max-width: 900px;
    margin-left: auto;
    margin-right: auto;
}

.chat-history {
    max-height: 60vh;
    overflow-y: auto;
    padding: 10px;
    border-radius: 12px;
    border: 1px solid var(--gray-100);
    background-color: var(--color-bg);
}

/* User message bubble */
.user-msg {
    background-color: #1E90FF;
    color: white;
    padding: 12px 16px;
    border-radius: 18px 18px 0 18px;
    max-width: 70%;
    margin-bottom: 8px;
    margin-left: auto;
}

/* Bot message bubble */
.bot-msg {
    background-color: #F1F0F0;
    color: black;
    padding: 14px 18px;
    border-radius: 18px 18px 18px 0;
    max-width: 70%;
    margin-bottom: 8px;
    margin-right: auto;
}

/* Centered welcome message */
.welcome-msg {
    text-align: center;
    font-size: 2rem;
    color: var(--dl-color-gray-900);
    margin-top: 3rem;
    margin-bottom: 2rem;
    font-weight: 600;
}
            
@keyframes fadeInSlideUp {
  0% {
    opacity: 0;
    transform: translateY(10px);
  }
  100% {
    opacity: 1;
    transform: translateY(0);
  }
}

.chat-bubble-anim {
  animation: fadeInSlideUp 2s ease forwards;
  animation-fill-mode: forwards;
}


</style>
""", unsafe_allow_html=True)



# Centered welcome message
st.markdown('<div class="welcome-msg">Welcome to DevOps Chatbot? how can I help you?</div>', unsafe_allow_html=True)

# Initialize chat history in session state
if "history" not in st.session_state:
    st.session_state.history = []


#sidebar
with st.sidebar:
    # Sidebar header
    st.header("Settings")
    if st.button("Reset Chat"):
        st.session_state.history = []
    # Display total number of messages
    st.markdown(f"**Total messages:** {len(st.session_state.history)}")

    # Display last question
    if st.session_state.history:
        last_user = st.session_state.history[-1][0]
        st.markdown(f"**Last question:** {last_user}")
    # Display recent questions    
    st.subheader("Recent questions")
    max_items = 10
    for i, (user_msg, _) in enumerate(reversed(st.session_state.history[-max_items:])):
        st.markdown(f"{i+1}. {user_msg[:50]}{'...' if len(user_msg) > 50 else ''}")
    st.markdown("---")
    # Theme selection
    theme = st.radio("Select Theme", ["Light", "Dark"], index=0)

    # Footer
    st.markdown("Made by Rudra Tyagi. Powered by Google Gemini and LangChain.")

# Inject theme-specific CSS overrides based on user selection
if theme == "Dark":
    st.markdown(f"""
    <style>
    body, .block-container {{
        background-color: #121212 !important;
        color: #eeeeee !important;
    }}
    .welcome-msg {{
        color: #eeeeee !important;
    }}
    .user-msg {{
        background-color: #0e4a72 !important;
        color: white !important;
    }}
    .bot-msg {{
        background-color: #333333 !important;
        color: white !important;
    }}
    </style>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
    <style>
    body, .block-container, .welcome-msg, .chat-history,
    .main, .appview-container,
    .st-emotion-cache-1wrcr25, .st-emotion-cache-18ni7ap,
    .st-emotion-cache-1kyxreq, .st-emotion-cache-q8sbsg {
        background: #fff !important;
        background-color: #fff !important;
        color: #000 !important;
    }
    .user-msg {
        background-color: #1E90FF !important;
        color: #fff !important;
    }
    .bot-msg {
        background-color: #F1F0F0 !important;
        color: #000 !important;
    }
    div[role="textbox"] {
        background: #fff !important;
        color: #000 !important;
    }
     
    </style>
    """, unsafe_allow_html=True)

#load document
pdf_path = Path("C:/Users/rudra/RAG-CHATBOT/data/devops.pdf")
docs = load_documents(str(pdf_path))

#split into chunks
chunks = split_documents(docs)

#build vectorstore
#texts = [chunk.page_content for chunk in chunks]
#embeddings = create_embeddings(texts)
retriever = build_vectorstore(chunks)

#Build Chains
rag_chain ,llm  = build_rag_chain(retriever)
followup = build_history_aware_chain(llm, retriever)

# Utility to extract answer safely
def extract_answer(response: dict) -> str:
    if isinstance(response, dict):
        for key in ["result", "answer", "output"]:
            if key in response:
                return response[key]
        return str(response)
    # If response is a raw string
    return str(response)


# Display chat history with styled chat bubbles and avatars
st.markdown('<div class="chat-history">', unsafe_allow_html=True)
for user_msg, bot_msg in st.session_state.history:
    user_html = f'<div class="user-msg chat-bubble-anim">{user_msg}</div>'
    bot_html = f'<div class="bot-msg chat-bubble-anim">{bot_msg}</div>'
    with st.chat_message("user", avatar="🧑"):
        st.markdown(user_html, unsafe_allow_html=True)
    with st.chat_message("assistant", avatar="🤖"):
        st.markdown(bot_html, unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)


# Persistent chat input at bottom
user_input = st.chat_input("Type your question here...")


#handle user input
if user_input:
    # Convert history to proper message format for LangChain
    def format_chat_history(history):
        formatted_history = []
        for user_msg, ai_msg in history:
            formatted_history.append(("human", user_msg))
            formatted_history.append(("ai", ai_msg))
        return formatted_history
    
    

    with st.spinner("Bot is typing..."):
    # Decide which chain to use
        if st.session_state.history:
        # Use followup chain - expects "input" and proper chat_history format
            chain = followup
            formatted_history = format_chat_history(st.session_state.history)
            result = chain.invoke({"input": user_input, "chat_history": formatted_history})
        else:
        # Use rag_chain - expects "query"
            chain = rag_chain
            result = chain.invoke({"query": user_input})

        answer = extract_answer(result)
    
    st.session_state.history.append((user_input, answer))

   
    # Display current conversation pair with styled bubbles and avatars
    user_html = f'<div class="user-msg chat-bubble-anim">{user_input}</div>'
    bot_html = f'<div class="bot-msg chat-bubble-anim">{answer}</div>'

    with st.chat_message("user", avatar="🧑"):
        st.markdown(user_html, unsafe_allow_html=True)

    with st.chat_message("assistant", avatar="🤖"):
        st.markdown(bot_html, unsafe_allow_html=True)