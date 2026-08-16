import os
from docx import Document
import PyPDF2

def extract_text_from_docx(file_obj):
    """Extract text from a .docx file-like object."""
    doc = Document(file_obj)
    text = []
    for paragraph in doc.paragraphs:
        text.append(paragraph.text)
    return '\n'.join(text)

def extract_text_from_pdf(file_obj):
    """Extract text from a .pdf file-like object."""
    text = ""
    reader = PyPDF2.PdfReader(file_obj)
    for page in reader.pages:
        text += page.extract_text() + "\n"
    return text

def handle_file_upload(uploaded_file):
    """Handle file upload and extract text based on file type."""
    file_extension = uploaded_file.name.split('.')[-1].lower()
    if file_extension == 'docx':
        return extract_text_from_docx(uploaded_file)
    elif file_extension == 'pdf':
        return extract_text_from_pdf(uploaded_file)
    else:
        raise ValueError("Unsupported file type. Please upload a .docx or .pdf file.")