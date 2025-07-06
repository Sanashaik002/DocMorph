import streamlit as st
from pdf2docx import Converter
from PyPDF2 import PdfReader
from pathlib import Path
import tempfile
import os
import io

st.title("📄 PDF ➜ Word Converter")
uploaded_file = st.file_uploader("Upload a PDF",type = ["pdf"])

if uploaded_file is not None:
    try:
        file_bytes = uploaded_file.read()
        pdf = PdfReader(io.BytesIO(file_bytes))
        st.write("✅PDF successfully uploaded!")
        st.write(f"Number of pages : {len(pdf.pages)}")
        with tempfile.NamedTemporaryFile(delete = False,suffix=".pdf") as temp_pdf:
            temp_pdf.write(file_bytes)
            temp_pdf.flush()
            os.fsync(temp_pdf.fileno())
            temp_pdf_path = temp_pdf.name

        word_path = temp_pdf_path.replace(".pdf",".docx")
        # Create Streamlit progress bar
        progress_bar = st.progress(0)
        status_text = st.empty()
        # Progress callback
        def update_progress(page,total):
            pct = int((page+1)/total * 100)
            progress_bar.progress(pct)
            status_text.text(f"Converting page {page + 1} of {total}...")
        # Convert PDF to Word with progress
        word_path = temp_pdf_path.replace(".pdf", ".docx")
        cv = Converter(temp_pdf_path)
        try:
            cv.convert(word_path, start=0, end=None, progress_bar=update_progress)
            cv.close()
        except Exception as inner_e:
            st.error(f"Conversion failed: {inner_e}")
            os.remove(temp_pdf_path)
            st.stop()

        # Read and offer download
        with open(word_path, "rb") as f:
            word_data = f.read()
        st.success("Conversion Completed!")
        custom_name = st.text_input("Enter a name for your Word file (without extension):")
        st.download_button(
            "Download Converted Word File",
            data = word_data,
            file_name=f"{custom_name}.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )
        #cleanup
        os.remove(temp_pdf_path)
        os.remove(word_path)
    except Exception as e:
        st.error(f"Conversion failed: {e}")

else:
    st.info("Please upload a PDF to begin.")