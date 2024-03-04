# main.py
from fastapi import FastAPI, File, UploadFile
import PyPDF2

app = FastAPI()

@app.post("/extract_text")
async def extract_text_from_pdf(pdf_file: UploadFile):
    try:
        # Save the uploaded PDF temporarily
        with open("temp.pdf", "wb") as temp_pdf:
            temp_pdf.write(pdf_file.file.read())

        # Extract text from the PDF
        with open("temp.pdf", "rb") as pdf:
            pdf_reader = PyPDF2. PdfReader(pdf)
            data = ""
            for i in pdf_reader.pages:
                data += i.extract_text() + "\n"

        return {"text": data}
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
