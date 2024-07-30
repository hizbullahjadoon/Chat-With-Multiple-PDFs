# -*- coding: utf-8 -*-
"""
Created on Tue Jul 16 14:00:37 2024
@author: USER
"""

import os
import streamlit as st
import pickle
import time
import langchain
import pandas as pd
from io import StringIO
from langchain.llms import GooglePalm
from langchain.chains import RetrievalQAWithSourcesChain, RetrievalQA
from langchain.chains.qa_with_sources.loading import load_qa_with_sources_chain
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import UnstructuredURLLoader, TextLoader
from langchain_community.embeddings import HuggingFaceInstructEmbeddings
from langchain.docstore.document import Document
from langchain.vectorstores import FAISS
import streamlit as st
from io import StringIO
import pprint
import google.generativeai as palm
import PyPDF2
from htmlTemplate import user_template, bot_template, css
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain

st.set_page_config(page_title="Chat with Multiple PDFs", page_icon=":books:")
st.write(css, unsafe_allow_html=True)

if "conversation" not in st.session_state:
    st.session_state.conversation = None

if "chat_history" not in st.session_state:
    st.session_state.chat_history = None

def load_and_split_pdf(file):
    reader = PyPDF2.PdfReader(file)
    pages = []
    for page_num in range(len(reader.pages)):
        page = reader.pages[page_num]
        pages.append(page.extract_text())
    return pages

def merge_pdf(pages):
    whole_text = " "
    for text in pages:
        whole_text += text
    return whole_text

def initial_config():
    google_api_key="Your Google Palm API Key"
    palm.configure(api_key=google_api_key)
    llm = GooglePalm(temperature=0.7, google_api_key=google_api_key)
    return llm

def handle_query(user_question):
    try:
        response = st.session_state.conversation({'question': user_question})
        #st.write(response)
        st.session_state.chat_history = response['chat_history']

        for i, message in enumerate(st.session_state.chat_history):
            if i % 2 == 0:
                st.write(user_template.replace("{{MSG}}", message.content), unsafe_allow_html=True)
            if i % 2 != 0:
                st.write(bot_template.replace("{{MSG}}", message.content), unsafe_allow_html=True)
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")

def get_conversation_chain(vectorIndex):
    llm = initial_config()
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    conversation_chain = ConversationalRetrievalChain.from_llm(llm=llm, retriever=vectorIndex.as_retriever(), memory=memory)
    return conversation_chain

st.header("Chat With Multiple PDFs :books:")
query = st.text_input("Question: ")
if query:
    handle_query(query)

llm = initial_config()

main_holder = st.empty()
string_data = ""
vec = ""

result = {"query": " ", "result": " "}

with st.sidebar:
    st.subheader("Upload a File")
    uploaded_files = st.sidebar.file_uploader("Choose a file", accept_multiple_files=True, type="pdf")
    process_url_clicked = st.sidebar.button("Process PDF(s)")
    if process_url_clicked:
        with st.spinner("Processing"):
            if uploaded_files is not None:
                for file in uploaded_files:
                    pages = load_and_split_pdf(file)
                    merged_text = merge_pdf(pages)
                    string_data += merged_text
                
                docs = [Document(page_content=string_data, metadata={"source": "source1"})]
                r_splitter = RecursiveCharacterTextSplitter(separators=['\n\n', '\n', ' '], chunk_size=200, chunk_overlap=20)
                split_docs = r_splitter.split_documents(docs)
                st.sidebar.write(split_docs)

                embeddings = HuggingFaceInstructEmbeddings()
                vectorIndex = FAISS.from_documents(split_docs, embeddings)
                st.session_state.conversation = get_conversation_chain(vectorIndex)
                st.success("File(s) processed successfully!")
