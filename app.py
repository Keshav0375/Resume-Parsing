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

        job_description = st.text_area("Enter Job Description Here:")

        if st.button("Evaluate Resume"):
            result = evaluate_resume(response, job_description)
            st.write("Evaluation Result:")
            st.write(result["JD Match"])
            st.write(result["MissingKeywords"])
            st.write(result["Profile Summary"])


def extract_text_from_pdf(pdf_file):
    url = "http://127.0.0.1:8000/extract_text"
    files = {"pdf_file": pdf_file}
    try:
        response = requests.post(url, files=files)
        return response.json()
    except Exception as e:
        return {"error": str(e)}


def evaluate_resume(resume_text, job_description):
    url = "http://localhost:8000/evaluate_resume"
    data = {"resume_text": resume_text, "job_description": job_description}
    response = requests.post(url, data=data)
    return response.json()

if __name__ == "__main__":
    main()
