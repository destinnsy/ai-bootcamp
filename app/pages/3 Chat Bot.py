import streamlit as st
from helper.rag import prompt_chatbot
from langchain_core.messages import HumanMessage, SystemMessage
from helper.utility import check_password

# Do not continue if check_password is not True.  
if not check_password():  
    st.stop()


st.title("Chat Bot")

st.write("This is a POC to build a RAG that can answer what are the security policies related to a piece of technology.")
st.write("Sample input: \"What are the security policies related to Kubernetes?\".")


if "chat_bot_messages" not in st.session_state:
    st.session_state.chat_bot_messages = []

chat_icon_mapping = {
    "human": "user",
    "system": "assistant"
}
for message in st.session_state.chat_bot_messages:
    with st.chat_message(chat_icon_mapping[message.type]):
        st.markdown(message.content)

if prompt := st.chat_input("What is up?"):
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        response = prompt_chatbot(prompt, st.session_state.chat_bot_messages)
        st.markdown(response["answer"])

    st.session_state.chat_bot_messages.extend([HumanMessage(content=prompt), SystemMessage(content=response["answer"])])