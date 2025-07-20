import streamlit as st
from langchain.llms import Ollama  # Import the Ollama class from Langchain
# pip install langchain langchain-community

st.title("Local LLM with Langchain!")

# Input for the prompt
prompt = st.text_area(label="Write your prompt.")
button = st.button("Okay")

if button:
    if prompt:
        # Initialize the local LLM
        llm = Ollama(model='llama3.1:8b')  # Specify your model here

        # Generate a response using the local LLM
        response = llm(prompt)

        # Display the response
        st.markdown(response)