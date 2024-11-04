from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_openai import ChatOpenAI
from langchain.chains.history_aware_retriever import create_history_aware_retriever
from langchain.chains.retrieval import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
import streamlit as st
from .data import good_to_have, should_have, must_have


embeddings_model = OpenAIEmbeddings(model='text-embedding-3-large')
vectordb = Chroma(
    embedding_function=embeddings_model,
    collection_name="IM8",
    persist_directory='./vector_db'
)

def prompt_chatbot(input: str, chat_history):
    retriever = vectordb.as_retriever()
    llm = ChatOpenAI(model=st.secrets["OPENAI_MODEL_NAME"], temperature=0)

    ### Contextualize question ###
    contextualize_q_system_prompt = """Given a chat history and the latest user question \
    which might reference context in the chat history, formulate a standalone question \
    which can be understood without the chat history. Do NOT answer the question, \
    just reformulate it if needed and otherwise return it as is."""
    contextualize_q_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", contextualize_q_system_prompt),
            MessagesPlaceholder("chat_history"),
            ("human", "{input}"),
        ]
    )
    history_aware_retriever = create_history_aware_retriever(
        llm, retriever, contextualize_q_prompt
    )


    ### Answer question ###
    qa_system_prompt = """You are an assistant for answering questions regarding software security policies. \
    Your task is to help the human better understand the security policies. \
    If the user is referring to a specific technology name, generate the response base on related information of that technology \
    In the event that the user only specifies a technology name without going into details, remember that your task is to answer what security policies are necessary for the specific technology. \
    If the user specifies a specific security level, only respond with the policies in that security level. \
    Use the following pieces of retrieved context to answer the question.
    
    If there are no policies within the user's specified security level, say that there is no related policy. \
    If you don't know the answer, just say that you don't know. \
    
    Each policy document has a field `id`. 
    Enclosed in the tag <profiles> states the 3 security levels: should have, must have and good to have.
    Each security level has a list of `id` under the policy.

    When answering, format your response in the following format:
    1. Policy name (seucirty level - id)
        - Statement:
        - Guidance: 

    <profiles>
    good to have: [{good_to_have}]
    should have: [{should_have}]
    must have: [{must_have}]
    </profiles>

    {context}"""
    qa_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", qa_system_prompt),
            MessagesPlaceholder("chat_history"),
            ("human", "{input}"),
        ]
    )
    question_answer_chain = create_stuff_documents_chain(llm, qa_prompt)

    rag_chain = create_retrieval_chain(retriever, question_answer_chain)

    response = rag_chain.invoke({"input": input, "chat_history": chat_history, "good_to_have": ','.join(good_to_have), "should_have": ','.join(should_have), "must_have": ','.join(must_have)})

    return response
