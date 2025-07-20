import streamlit as st
from langchain.llms import Ollama
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

st.title("Local LLM with Langchain!")

# Input for the prompt
prompt = st.text_area(label="Write your prompt.")
button = st.button("Okay")

if button:
    if prompt:
        # Initialize the local LLM
        llm = Ollama(model='llama3.1:8b')  # Specify your model here

        # Define the prompt template
        template = """You are a helpful assistant. You have been asked the following question:

Question: {question}

Please provide a detailed and thoughtful response as a list with short items.
"""
        prompt_template = PromptTemplate(template=template, input_variables=["question"])

        # Create the LLMChain
        chain = LLMChain(llm=llm, prompt=prompt_template)

        # Generate a response using the LLMChain
        response = chain.run(prompt)

        # Display the response
        st.markdown(response)