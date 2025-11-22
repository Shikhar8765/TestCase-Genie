# 🤖 Autonomous QA Agent

### *Automated Test Case Generation & Selenium Script Builder using RAG + Gemini AI*

**Author:** **Shikhar Srivastava**
**Registration Number:** **22BCE10172**
**Course:** Assignment – Autonomous QA Agent (Assignment-1)

---

## 📘 Overview

This project implements an **Autonomous QA Agent** capable of:

### ✅ 1. Building a Knowledge Base

Uploads PDF/TXT/MD/JSON/HTML files and converts them into vector embeddings using **ChromaDB + Sentence Transformers**.

### ✅ 2. Generating Test Cases

Uses **Google Gemini (1.5 Flash)** + RAG to generate **context-aware JSON test cases**.

### ✅ 3. Generating Selenium Scripts

Creates **fully functional Python Selenium scripts**, grounded in real selectors extracted from `checkout.html`.

The system works end-to-end and produces **industry-quality QA automation outputs**.

---

## 🏗️ Tech Stack

| Component    | Technology                             |
| ------------ | -------------------------------------- |
| Frontend     | Streamlit                              |
| Backend      | FastAPI                                |
| Vector DB    | ChromaDB                               |
| Embeddings   | sentence-transformers/all-MiniLM-L6-v2 |
| LLM          | Google Gemini API                      |
| HTML Parsing | BeautifulSoup                          |
| Automation   | Selenium WebDriver                     |
| RAG          | Custom Retriever + Embeddings          |

---

## 📁 Project Structure

```
autonomous-qa-agent/
│
├── backend/
│   ├── main.py
│   ├── ingestion.py
│   ├── vector_engine.py
│   ├── test_case_agent.py
│   ├── selenium_agent.py
│   ├── assets/
│   │     └── checkout.html
│   └── storage/
│         ├── vector_db/
│         └── uploaded_files/
│
├── frontend/
│   └── app.py
│
├── documentation/
│   └── Assignment-1.pdf
│
├── README.md
└── requirements.txt
```

---

## ⚙️ Installation

### **1️⃣ Create Virtual Environment**

```
python -m venv venv
```

Activate:

**Windows**

```
venv\Scripts\activate
```

**Mac/Linux**

```
source venv/bin/activate
```

---

### **2️⃣ Install Dependencies**

```
pip install -r requirements.txt
```

---

## ▶️ Running the Project

### **Start Backend**

```
uvicorn backend.main:app --reload
```

Backend will run at:
👉 [http://localhost:8000/docs](http://localhost:8000/docs)

---

### **Start Frontend**

```
streamlit run frontend/app.py
```

Frontend will run at:
👉 [http://localhost:8501](http://localhost:8501)

---

## 🧪 How to Use

### **Step 1 — Upload Files**

Upload:

* Assignment PDF
* checkout.html
* Any project-related docs

Click **Build Knowledge Base** → system ingests files & stores embeddings.

---

### **Step 2 — Generate Test Cases**

Enter a query such as:

```
discount code validation
login flow
payment form submission
```

Result → Structured JSON test cases appear instantly.

---

### **Step 3 — Generate Selenium Script**

Choose any test case from the dropdown.
System generates a **Python Selenium script** using only selectors in checkout.html.

---

## 🤖 LLM Configuration (Gemini)

```python
import google.generativeai as genai
genai.configure(api_key="YOUR_API_KEY")
model = genai.GenerativeModel("gemini-1.5-flash")
```

---

## 🎥 Assignment Requirement – Video Demo

You must submit:

✔ GitHub Repository
✔ A **video demo (< 15 mins)** uploaded to Google Drive
✔ Show working frontend + backend
✔ Explain code, workflow, and RAG pipeline

Deployment is optional but gives **extra marks**.

---

## 🚀 Deployment (Optional for Extra Marks)

### Backend → Railway.app

Start Command:

```
uvicorn backend.main:app --host 0.0.0.0 --port $PORT
```

### Frontend → Streamlit Cloud / Render

---

## 👨‍🎓 Student Info

**Name:** Shikhar Srivastava
**Reg No:** 22BCE10172
**University:** VIT Bhopal University

---

## ⭐ Final Notes

This project demonstrates mastery over:

✔ FastAPI
✔ Streamlit
✔ Vector Databases
✔ Embeddings
✔ Gemini LLMs
✔ RAG
✔ Automated Selenium Script Generation

A complete industry-standard QA automation agent.

