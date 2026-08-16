import streamlit as st
import ollama

st.title("Ollama!")
prompt = st.text_area(label = "Write your prompt.")
button = st.button("Okay")

if button:
    if prompt:
        response = ollama.generate(model='llama3.1:8b', prompt=prompt)
        st.markdown(response["response"])