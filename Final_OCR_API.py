from fastapi import FastAPI, File, UploadFile, Form
from pdf2image import convert_from_bytes
import easyocr
import numpy as np
import io
import os
import json
from dotenv import load_dotenv
import google.generativeai as genai


app = FastAPI()

# Initialize the OCR reader
reader = easyocr.Reader(['en'])

load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


def get_gemini_repsonse(input):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(input)
    return response.text


@app.post("/extract_text")
async def extract_text(file: UploadFile = File(...)):
    # Read the contents of the uploaded file
    contents = await file.read()

    # Check file extension to determine the file type
    file_extension = file.filename.split('.')[-1].lower()

    if file_extension == 'pdf':
        # Convert PDF contents to images
        images = await convert_pdf_to_images(contents)
    elif file_extension in ['jpg', 'jpeg', 'png']:
        # Process image directly
        images = [np.array(contents)]
    else:
        return {"error": "Unsupported file type. Please upload a PDF, JPG, or PNG."}

    # Extract text from images
    extracted_text = await extract_text_from_images(images)

    return {"extracted_text": extracted_text}


async def convert_pdf_to_images(pdf_contents: bytes):
    images = []
    pdf_images = convert_from_bytes(pdf_contents)
    for image in pdf_images:
        images.append(np.array(image))
    return images


async def extract_text_from_images(images):
    text = ""
    for image in images:
        bounds = reader.readtext(image)
        for i in range(len(bounds)):
            text += bounds[i][1] + '\n'
    return text


@app.post("/evaluate_resume")
async def evaluate_resume(resume_text: str = Form(...), job_description: str = Form(...)):
    # Call the Gemini model with the formatted input
    input = f"""
    Hey Act Like a skilled or very experience ATS(Application Tracking System)
    with a deep understanding of tech field,software engineering,data science ,data analyst
    and big data engineer. Your task is to evaluate the resume based on the given job description.
    You must consider the job market is very competitive and you should provide 
    best assistance for improving thr resumes. Assign the percentage Matching based 
    on Jd and
    the missing keywords with high accuracy
    resume:{resume_text}
    description:{job_description}

    I want the response in one single string having the structure
    {{"JD Match":"%","MissingKeywords:[]","Profile Summary":""}}
    """
    response = get_gemini_repsonse(input)

    # Parse the response string into a dictionary
    response_dict = json.loads(response)

    return response_dict
