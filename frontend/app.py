import streamlit as st
import requests
import json
import re

BACKEND_URL = "http://localhost:8000"

st.set_page_config(page_title="Autonomous QA Agent", layout="wide")

st.title("🤖 Autonomous QA Agent for Test Case & Selenium Script Generation")
st.write("Upload documents, build knowledge base, generate test cases, and produce Selenium scripts.")


# -----------------------------------------
# Helper: Clean LLM JSON (remove ```json fences)
# -----------------------------------------
def clean_llm_json(text):
    if not text:
        return ""

    # Remove markdown code fences like ```json or ```
    text = re.sub(r"```json", "", text, flags=re.IGNORECASE)
    text = text.replace("```", "")

    # Trim whitespace
    return text.strip()



# -----------------------------
# SECTION 1: UPLOAD DOCUMENTS
# -----------------------------
st.header("📂 1. Upload Support Documents + checkout.html")

uploaded_files = st.file_uploader(
    "Upload PDF, TXT, MD, JSON, or checkout.html",
    type=["pdf", "txt", "md", "json", "html"],
    accept_multiple_files=True
)

if st.button("Build Knowledge Base"):
    if uploaded_files:
        files_to_send = []
        for f in uploaded_files:
            files_to_send.append(
                ("files", (f.name, f.getvalue(), f"type"))
            )

        response = requests.post(f"{BACKEND_URL}/upload_files", files=files_to_send)

        if response.status_code == 200:
            st.success("Knowledge Base Built Successfully!")
        else:
            st.error("Error while building knowledge base!")
    else:
        st.warning("Please upload at least one file.")


# -----------------------------
# SECTION 2: GENERATE TEST CASES
# -----------------------------
st.header("🧪 2. Generate Test Cases")

query = st.text_input("Enter feature or module (e.g., 'discount code', 'payment flow', 'user form').")

if st.button("Generate Test Cases"):
    if query.strip() != "":
        response = requests.post(
            f"{BACKEND_URL}/generate_test_cases",
            data={"query": query}
        )

        if response.status_code == 200:
            raw_output = response.json()["test_cases"]

            st.subheader("Generated Test Cases (Raw LLM Output):")
            st.code(raw_output, language="json")

            # Clean JSON before saving
            cleaned_json = clean_llm_json(raw_output)
            st.session_state["testcases_raw"] = cleaned_json
        else:
            st.error("Backend error!")
    else:
        st.warning("Enter a test case query.")


# -----------------------------
# SECTION 3: SELECT TEST CASE & GENERATE SCRIPT
# -----------------------------
st.header("⚙️ 3. Generate Selenium Script from Test Case")

if "testcases_raw" in st.session_state:

    try:
        parsed_list = json.loads(st.session_state["testcases_raw"])
    except Exception as e:
        st.error(f"LLM output is not valid JSON. Error: {e}")
        parsed_list = []

    if parsed_list:
        options = [json.dumps(item, indent=2) for item in parsed_list]
        selected_case = st.selectbox("Select a Test Case:", options)

        if st.button("Generate Selenium Script"):
            response = requests.post(
                f"{BACKEND_URL}/generate_selenium_script",
                data={"testcase_json": selected_case}
            )

            if response.status_code == 200:
                script = response.json()["selenium_script"]
                st.subheader("Generated Selenium Script:")
                st.code(script, language="python")
            else:
                st.error("Error while generating script.")
    else:
        st.warning("No valid JSON test cases found.")

else:
    st.info("Generate test cases first to enable this section.")
