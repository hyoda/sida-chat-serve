import os
import random
import openai
import streamlit as st
import numpy as np
from streamlit_chat import message
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma

DB_DIR = "./db/"

db = Chroma(
    embedding_function=HuggingFaceEmbeddings(model_name="jhgan/ko-sbert-sts"),
    persist_directory=DB_DIR,
)

openai.api_key = st.secrets['pass']

st.title("시다 챗: 남해워케이션에서 만든 인공지능 챗봇")

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    doc = db.similarity_search(prompt, k=25)
    doc = [x.page_content for x in doc if len(x.page_content) > 80]
    ref_content = "\n\n".join(random.choices(doc, k=min(9, len(doc))))
    
    ref_prompt = f"""
    <reference>{ref_content}</reference>\n
    reference를 참고해서 답변합니다. 최종 정답만 말합니다.
    ---
    {prompt}"""

    with st.chat_message("assistant"):
        message_placeholder = st.empty()

        full_response = ""
        for response in openai.ChatCompletion.create(
            model=st.session_state["openai_model"],
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages[:-1]
            ] + [{"role": "user", "content": ref_prompt}],
            stream=True,
        ):
            full_response += response.choices[0].delta.get("content", "")
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)
    st.session_state.messages.append({"role": "assistant", "content": full_response})