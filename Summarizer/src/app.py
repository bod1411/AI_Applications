import streamlit as st
from summarizer import summarize_text
from utils.file_handler import handle_file_upload

def main():
    st.title("Text Summarizer")
    st.write("Enter text or upload a file (Word, PDF) to get a summary.")

    # Text input
    text_input = st.text_area("Enter text here:")

    # File upload
    uploaded_file = st.file_uploader("Upload a file", type=["pdf", "docx"])

    if st.button("Summarize"):
        if text_input:
            summary = summarize_text(text_input)
            st.subheader("Summary:")
            st.write(summary)
        elif uploaded_file:
            file_text = handle_file_upload(uploaded_file)
            summary = summarize_text(file_text)
            st.subheader("Summary:")
            st.write(summary)
        else:
            st.warning("Please enter text or upload a file.")

if __name__ == "__main__":
    main()