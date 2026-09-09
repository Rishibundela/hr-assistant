"""
Streamlit app for the HR Assistant RAG application.
Run with: `streamlit run app.py`
"""

import streamlit as st
from hr_assistant.pipeline import build_hr_assistant, ask_assistant 
from hr_assistant.logger import get_logger

logger = get_logger(__name__)

st.set_page_config(page_title="HR Assistant", page_icon="🤖")
st.title("HR Policy Assistant")
st.caption("Ask any questions about the company HR policies!")

@st.cache_resource(show_spinner="Building the HR assistant...")
def get_hr_assistant():
    """Build and return the HR assistant agent."""
    return build_hr_assistant()

agent = get_hr_assistant()

if 'messages' not in st.session_state:
    st.session_state.messages = []

# for the past messages, display them in the chat interface
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# get user question
question = st.chat_input("Ask a question about the HR policies")

if question:
    logger.info(f"Streamlit run: User Question: {question}")
    # display user message in chat message container
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.markdown(question)

    # display assistant response in chat message container
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            answer = ask_assistant(agent, question)
        st.markdown(answer)
    st.session_state.messages.append({"role": "assistant", "content": answer})
            