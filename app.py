import os
import subprocess
import streamlit as st
import re
import fitz  # PyMuPDF for PDF
from docx import Document

# Ensure required dependencies are installed
def install_missing_packages():
    required_packages = ["pymupdf", "python-docx"]
    for package in required_packages:
        try:
            __import__(package.replace("-", "_"))
        except ImportError:
            subprocess.run(["pip", "install", package], check=True)

install_missing_packages()

# Function to Extract Text from TXT
def extract_text_from_txt(uploaded_file):
    return uploaded_file.getvalue().decode("utf-8").strip()

# Function to Extract Text from PDF
def extract_text_from_pdf(uploaded_file):
    try:
        with fitz.open(stream=uploaded_file.read(), filetype="pdf") as doc:
            text = "\n".join([page.get_text() for page in doc])
        return text.strip()
    except Exception as e:
        return f"Error extracting text from PDF: {str(e)}"

# Function to Extract Text from DOCX
def extract_text_from_docx(uploaded_file):
    try:
        doc = Document(uploaded_file)
        text = "\n".join([para.text for para in doc.paragraphs])
        return text.strip()
    except Exception as e:
        return f"Error extracting text from DOCX: {str(e)}"

# Function to Extract Specific Sections
def extract_section(text, section):
    section_patterns = {
        "Skills": r"(?:Skills|Technical Skills|Key Skills)[\s:|\-]*(.*?)(?=\n\n|\Z)",
        "Projects": r"(?:Projects|Academic Projects|Work Projects)[\s:|\-]*(.*?)(?=\n\n|\Z)",
        "Work Experience": r"(?:Work Experience|Professional Experience)[\s:|\-]*(.*?)(?=\n\n|\Z)",
        "Education": r"(?:Education|Academic Background|Qualification)[\s:|\-]*(.*?)(?=\n\n|\Z)"
    }

    pattern = section_patterns.get(section)
    if pattern:
        match = re.search(pattern, text, re.DOTALL | re.IGNORECASE)
        return match.group(1).strip() if match else f"No {section} found!"
    return "Invalid section selected."

# Streamlit UI
st.title("NinjaGist 🥷⚡ – Your AI-Powered Summarization Sensei!")
st.markdown("<h1 style='text-align: center;'>📝 GistNinja 🥷 - Cutting Through Text Like a Pro! 🤖📄</h1>", unsafe_allow_html=True)

# File Uploader (PDF, DOCX, TXT)
uploaded_file = st.file_uploader("Upload Your Resume (PDF, DOCX, TXT)", type=["pdf", "docx", "txt"])

if uploaded_file:
    file_type = uploaded_file.name.split(".")[-1]

    if file_type == "txt":
        text = extract_text_from_txt(uploaded_file)
    elif file_type == "pdf":
        text = extract_text_from_pdf(uploaded_file)
    elif file_type == "docx":
        text = extract_text_from_docx(uploaded_file)
    else:
        st.error("Unsupported file format!")
        st.stop()

    st.text_area("Extracted Resume Text", text, height=250)  # Debugging

    st.subheader("🎯 Select a Section to Extract:")
    section = st.selectbox("Choose Summary Type:", ["Skills", "Projects", "Work Experience", "Education"])

    if st.button("🔍 Extract Summary"):
        summary = extract_section(text, section)
        st.markdown(f"### ✨ {section} Summary:")
        st.write(summary)

        # Download Button
        st.download_button(
            label="📥 Download Summary",
            data=summary,
            file_name=f"{section}_summary.txt",
            mime="text/plain"
        )
# Footer
st.markdown("---")
st.markdown("<p style='text-align:center;'>🚀 Powered by Khushi & GistNinja 🥷</p>", unsafe_allow_html=True)
