import textwrap
import streamlit as st

from faq_bot import FAQBot

st.set_page_config(page_title="Sportswear FAQ Chatbot", page_icon="🧢")

# Path to your FAQ file
FAQ_PATH = "faq(1).xlsx"   # Use your actual file name here

# Load FAQ bot once
@st.cache_resource
def load_faq_bot():
    return FAQBot(FAQ_PATH)

faq_bot = load_faq_bot()

# -----------------------------------------
# MAIN UI
# -----------------------------------------
st.title("🏟️ Sportswear and Jersey FAQ Chatbot")

st.caption(
    "Ask questions about jerseys, bulk orders, customization, sizes, delivery, payment and more."
)

st.sidebar.title("Info")
st.sidebar.write("This chatbot uses your predefined FAQ Excel file and embeddings.")
st.sidebar.write(f"FAQ file: `{FAQ_PATH}`")
st.sidebar.write("Answers are selected based on similarity to your stored questions.")

# Chat history in session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Show previous messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Input
user_input = st.chat_input("Type your question about jerseys or orders")

if user_input:
    # User message
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Bot answer from FAQ embeddings
    bot_reply = faq_bot.answer(user_input)

    st.session_state.messages.append({"role": "assistant", "content": bot_reply})
    with st.chat_message("assistant"):
        st.markdown(bot_reply)
