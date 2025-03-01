import os
import streamlit as st

# Install pymupdf if not found
try:
    import pymupdf
except ModuleNotFoundError:
    os.system("pip install pymupdf")
    import pymupdf

import re
import io
from docx import Document

# Function to Extract Text from TXT
def extract_text_from_txt(uploaded_file):
    return uploaded_file.getvalue().decode("utf-8").strip()

# Function to Extract Text from PDF
def extract_text_from_pdf(uploaded_file):
    pdf_bytes = io.BytesIO(uploaded_file.read())  # Convert file to bytes
    doc = pymupdf.open(stream=pdf_bytes, filetype="pdf")
    text = "\n".join([page.get_text("text") for page in doc])
    return text.strip()

# Function to Extract Text from DOCX
def extract_text_from_docx(uploaded_file):
    doc = Document(uploaded_file)
    text = "\n".join([para.text for para in doc.paragraphs])
    return text.strip()

# Streamlit UI
st.title("📄 Resume Section Extractor")
uploaded_file = st.file_uploader("Upload Your Resume (PDF, DOCX, TXT)", type=["pdf", "docx", "txt"])

if uploaded_file:
    file_type = uploaded_file.name.split(".")[-1].lower()

    if file_type == "txt":
        text = extract_text_from_txt(uploaded_file)
    elif file_type == "pdf":
        text = extract_text_from_pdf(uploaded_file)
    elif file_type == "docx":
        text = extract_text_from_docx(uploaded_file)
    else:
        st.error("Unsupported file format!")
        st.stop()

    st.text_area("Extracted Resume Text", text[:5000], height=250)
