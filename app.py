# app.py
import streamlit as st
import requests

def main():
    st.title("Resume Text Extractor")

    uploaded_file = st.file_uploader("Upload a PDF resume", type=["pdf"])

    if uploaded_file:
        st.write("File uploaded successfully!")
        st.write("Extracted text:")
        response = extract_text_from_pdf(uploaded_file)
        st.write(response["text"])

def extract_text_from_pdf(pdf_file):
    url = "http://127.0.0.1:8000/extract_text"
    files = {"pdf_file": pdf_file}
    try:
        response = requests.post(url, files=files)
        return response.json()
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    main()
