import streamlit as st
import requests
import time


@st.cache_data()
def extract_text_from_file(file):
    url = "http://localhost:8000/extract_text"
    files = {"file": file}
    response = requests.post(url, files=files)
    return response.json().get("extracted_text", "Error: No text extracted")


def evaluate_resume(resume_text, job_description):
    url = "http://localhost:8000/evaluate_resume"
    data = {"resume_text": resume_text, "job_description": job_description}
    response = requests.post(url, data=data)
    return response.json()

def main():
    st.title("Resume Evaluator")

    uploaded_file = st.file_uploader("Upload Resume (PDF or Image)", type=["pdf", "jpg", "jpeg", "png"])

    if uploaded_file:
        st.header("File uploaded successfully")
        time.sleep(7)
        st.header("Waiting for response")
        time.sleep(7)
        st.subheader("It will take 45 seconds")
        resume_text = extract_text_from_file(uploaded_file)
        st.write("Extracted Text from Resume:")
        st.write(resume_text)

        job_description = st.text_area("Enter Job Description Here:")
        time.sleep(7)
        st.header("Waiting for response")
        time.sleep(7)
        st.subheader("It will take 45 seconds")

        if st.button("Evaluate Resume"):

            result = evaluate_resume(resume_text, job_description)
            st.write("Evaluation Result:")
            st.write(result["JD Match"])
            st.write(result["MissingKeywords"])
            st.write(result["Profile Summary"])

if __name__ == "__main__":
    main()
