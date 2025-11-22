from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
import shutil
import os
import json

import google.generativeai as genai

from backend.ingestion import DocumentIngestion
from backend.test_case_agent import TestCaseAgent
from backend.selenium_agent import SeleniumAgent


# -----------------------------------------
# 1) Configure Gemini API
# -----------------------------------------
genai.configure(api_key="AIzaSyAcqml5Smo81_I714QzFMmxbTFquD_9SR4")

# Auto-select latest model — no model name required
model = genai.GenerativeModel("gemini-2.0-flash")
def LLM(prompt: str):
    """Gemini-powered LLM wrapper"""
    try:
        response = model.generate_content(prompt)

        if hasattr(response, "text"):
            return response.text

        return str(response)

    except Exception as e:
        return f"LLM ERROR: {e}"


# -----------------------------------------
# 2) Initialize FastAPI
# -----------------------------------------
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# -----------------------------------------
# 3) Upload Files + Build Knowledge Base
# -----------------------------------------
@app.post("/upload_files")
async def upload_files(files: list[UploadFile] = File(...)):
    storage_dir = "backend/storage/uploaded_files"
    os.makedirs(storage_dir, exist_ok=True)

    file_records = []

    for file in files:
        save_path = f"{storage_dir}/{file.filename}"
        with open(save_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        file_records.append((save_path, file.filename))

    ingestion = DocumentIngestion()
    msg = ingestion.build_knowledge_base(file_records)

    return {"status": "success", "message": msg}


# -----------------------------------------
# 4) Generate Test Cases (Uses Gemini)
# -----------------------------------------
@app.post("/generate_test_cases")
async def generate_test_cases(query: str = Form(...)):
    agent = TestCaseAgent()
    response = agent.generate_test_cases(query, LLM)
    return {"test_cases": response}


# -----------------------------------------
# 5) Generate Selenium Script (uses Gemini)
# -----------------------------------------
@app.post("/generate_selenium_script")
async def generate_selenium_script(testcase_json: str = Form(...)):
    agent = SeleniumAgent()
    script = agent.generate_script(testcase_json, LLM)
    return {"selenium_script": script}
