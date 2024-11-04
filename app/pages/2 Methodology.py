import streamlit as st
import os
from helper.utility import check_password

# Do not continue if check_password is not True.  
if not check_password():  
    st.stop()

st.title("Methodology")


chatbot_string = """
# Chatbot

Chatbot build on RAG using IM8 Reform's catalogue as the data set.

## Target outcomes

1. User can input a name of a technology and the chatbot should respond with what are the relevant policies for the piece of technology. Eg. "What are the policies related to DNS?"
1. User can input the security level that he wishes to know about. Eg. "What are the must have policies for DNS?"

## Pain points / Lessons learnt

### Brevity of documents

As the data source used (IM8-reform) is a highly summarised version of the original IM8 poilicy document, the data is too brief. As a result, RAG is having a hard time finding the relevant documents and would need to rely on text generation to elaborate on the point, resulting in inaccuracies in the output generated.

### Disjoint in data in documents resulting in hallucination

When trying to specify the security level of the policy to be returned, the RAG has a strong tendency to hallucinate. If you are querying on a technology that does not have anything in the spcific security level at all, (Eg. must have policies for SQS), it is able to identify that there are no relevant policies reasonabily accurately. However, when querying for a technology that has policies across different security level, it has a high tendency of hallucanating.

It is likely caused by the disjoint in data. As the list of 'must have', 'should have' and 'good to have' are provided seperately in a list of policy ids. There is a tendency for the LLM to mix up which id is under which category when multiple policies are involved in the output.

## Methodology

When extracting the metadata, while it is possible to do so by code as the data is in json, due to the irregularlity of the json structure, it was observed that it was more reliable to use LLM to extract the necessary data.
"""

st.markdown(chatbot_string)


cwd = os.getcwd()
st.image(f"{cwd}/app/pages/methodology_chatbot.png")

security_guide_string = """
# Security Guide

## Target outcomes

A new developer might not be aware of what are the common security misconfigurations and vulnerabilities.

This is an attempt to build a CrewAI agent that can search the internet for common misconfigurations and vulnerabilities and format the information into an easy to understand manner for the user.

## Pain points / Lesson learnt

As the key feature of this Crew Agent is to search the internet for informat to generate and it is dependent on a writer agent to write the information, it is difficult to ensure the consistancy of the generated output.

## Methodology
"""

st.markdown(security_guide_string)

st.image(f"{cwd}/app/pages/methodology_security_guide.png")