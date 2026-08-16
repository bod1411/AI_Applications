import streamlit as st
from langchain.llms import Ollama
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.text_splitter import RecursiveCharacterTextSplitter
import spacy


# Load the SpaCy model for embeddings
# spacy.cli.download("en_core_web_md")
nlp = spacy.load("en_core_web_md")

st.title("Chat with Your Note")


with st.form(key='my_form', clear_on_submit=True):
    # Input fields for the form
    note = st.text_area(label="Paste your note here.", height=300)
    # Submit button
    submit_button = st.form_submit_button(label='Save')

if submit_button:
    if note:
        with open("note.text", 'r') as file:  # 'r' mode opens the file for reading
            content = file.read()  # Read the entire content of the file
            if note not in content:
                content += f"\n\n{note}"
                with open("note.text", 'w') as file:  # 'w' mode opens the file for writing (overwrites existing content)
                    file.write(content)

question = st.text_input(label="Enter your question:")
button = st.button("ASK")
# st.markdown(f"{len(long_text)}")


if button:
    if question:
        # Initialize the local LLM
        llm = Ollama(model='llama3.1:8b')  # Specify your model here

        # Define the prompt template for summarization
        template = """You are a helpful assistant. Please answer the following question based on the below text:

Question: {question}

Text: {text}
"""
        prompt_template = PromptTemplate(template=template, input_variables=["text", "question"])

        with open("note.text", 'r') as file:  # 'r' mode opens the file for reading
            content = file.read()  # Read the entire content of the file
        # Split the long text into chunks using RecursiveCharacterTextSplitter
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)
        chunks = text_splitter.create_documents([content])

        # Initialize an empty list to store the similarities
        similarities = []
        # Generate a summary for each chunk
        for chunk in chunks:
            similarity_score = nlp(question).similarity(nlp(chunk.page_content))
            similarities.append((similarity_score, chunk.page_content))

            # # Create the LLMChain for each chunk
            # chain = LLMChain(llm=llm, prompt=prompt_template)
            # summary = chain.run(chunk.page_content)
            # summaries.append(summary)
            # chunk_contents.append(chunk.page_content)

        ordered_chunks = sorted(similarities, key=lambda x: x[0], reverse=True)[:3]

        text= ""
        for score, sentence in ordered_chunks:
            st.markdown(f"Similarity: {score:.4f} - Sentence: {sentence}")
            text += f"{sentence}\n\n"
        chain = LLMChain(llm=llm, prompt=prompt_template)
        answer = chain.run({"text": text,
                            "question": question})

        st.subheader("Answer:")
        st.markdown(answer)

