import streamlit as st
from io import BytesIO
from pdf2docx import Converter
from docx import Document
from fpdf import FPDF
import tempfile
import os

def pdf_to_word(pdf_file):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_pdf:
        temp_pdf.write(pdf_file.read())
        temp_pdf.flush()
        docx_path = temp_pdf.name.replace('.pdf', '.docx')
        cv = Converter(temp_pdf.name)
        cv.convert(docx_path, start=0, end=None)
        cv.close()
    with open(docx_path, "rb") as f:
        docx_bytes = f.read()
    os.remove(temp_pdf.name)
    os.remove(docx_path)
    return docx_bytes

def word_to_pdf(docx_file):
    doc = Document(docx_file)
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    for para in doc.paragraphs:
        text = para.text.encode('latin-1', 'replace').decode('latin-1')
        pdf.multi_cell(0, 10, text)
    pdf_bytes = BytesIO()
    pdf.output(pdf_bytes)
    pdf_bytes.seek(0)
    return pdf_bytes

st.title("PDF <-> Word Converter")

option = st.radio("Select conversion type:", ("PDF to Word", "Word to PDF"))

if option == "PDF to Word":
    pdf_file = st.file_uploader("Upload PDF file", type=["pdf"])
    if pdf_file and st.button("Convert to Word"):
        docx_bytes = pdf_to_word(pdf_file)
        st.success("Conversion successful!")
        # Get original file name without extension
        original_name = pdf_file.name.rsplit('.', 1)[0] if pdf_file.name else "converted"
        download_name = f"{original_name}.docx"
        st.download_button("Download Word file", docx_bytes, file_name=download_name)
elif option == "Word to PDF":
    docx_file = st.file_uploader("Upload Word file", type=["docx"])
    if docx_file and st.button("Convert to PDF"):
        pdf_bytes = word_to_pdf(docx_file)
        st.success("Conversion successful!")
        # Get original file name without extension
        original_name = docx_file.name.rsplit('.', 1)[0] if docx_file.name else "converted"
        download_name = f"{original_name}.pdf"
        st.download_button("Download PDF file", pdf_bytes, file_name=download_name)