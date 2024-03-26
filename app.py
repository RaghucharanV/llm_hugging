from getpass import getpass
from langchain.prompts import PromptTemplate
from langchain import HuggingFaceHub
from huggingface_hub import InferenceClient
from langchain.chains import LLMChain
import os
import streamlit as st
import random
import time



#HUGGINGFACEHUB_API_TOKEN = getpass()
os.environ["HUGGINGFACEHUB_API_TOKEN"] = "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"

st.title("A LLM based Chatbot")
st.subheader("with Hugging_face_")


llm = HuggingFaceHub(repo_id='declare-lab/flan-alpaca-large', model_kwargs={"temperature":0.1,"max_length":1024})



prompt = PromptTemplate(
    template="answer to the prompt : {product}",
    input_variables=['product']
)



chain = LLMChain(llm=llm,prompt=prompt)

if "messages" not in st.session_state:
    st.session_state.messages= []


for message in st.session_state.messages:
    with st.chat_message(message['role']):
        st.markdown(message["content"])


if prompt := st.chat_input("Question anything?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
        prom = prompt


    def response_generator(query):
        response =  chain.run(query)
        
        for word in response.split():
            yield word + " "
            time.sleep(0.05) #retrieval_chain.run(query)

    with st.chat_message("assistant"):
        response = st.write_stream(response_generator(prom))
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})
