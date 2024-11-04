from openai import OpenAI
import streamlit as st
from helper.crewai_bot import crewai_prompt
from langchain_core.messages import HumanMessage, SystemMessage


st.title("Security Guide")

st.write("This is a POC to build a Crew agent that can search the internet for common security misconfigurations and vulnerabilities when a technology is inputted.")
st.write("Sample input: \"iframes\".")

if "security_guide_messages" not in st.session_state:
    st.session_state.security_guide_messages = []

chat_icon_mapping = {
    "human": "user",
    "system": "assistant"
}
for message in st.session_state.security_guide_messages:
    with st.chat_message(chat_icon_mapping[message.type]):
        st.markdown(message.content)

if prompt := st.chat_input("What is up?"):
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        st.write("... Generating response, this may take up to a few minutes. If you see the Running... text at the top right of the browser please continue waiting for the response...")
        response = crewai_prompt(prompt)
        st.markdown(response)

    st.session_state.security_guide_messages.extend([HumanMessage(content=prompt), SystemMessage(content=response)])