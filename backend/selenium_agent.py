import json
import os
from bs4 import BeautifulSoup
from backend.vector_engine import VectorEngine

class SeleniumAgent:

    def __init__(self):
        # Auto-detect uploaded HTML
        upload_dir = "backend/storage/uploaded_files"
        html_files = [f for f in os.listdir(upload_dir) if f.endswith(".html")]

        if not html_files:
            raise FileNotFoundError("No HTML file found in uploaded_files folder. Upload checkout.html.")

        # Use the FIRST uploaded HTML file
        self.html_path = os.path.join(upload_dir, html_files[0])
        self.retriever = VectorEngine()

    def load_html(self):
        with open(self.html_path, "r", encoding="utf-8") as f:
            html = f.read()
        return html, BeautifulSoup(html, "html.parser")

    def extract_selectors(self, soup):
        selectors = []

        # Extract IDs
        for tag in soup.find_all(attrs={"id": True}):
            selectors.append({
                "type": "id",
                "value": tag.get("id"),
                "tag": tag.name,
                "text": tag.text.strip()
            })

        # Extract NAME attributes
        for tag in soup.find_all(attrs={"name": True}):
            selectors.append({
                "type": "name",
                "value": tag.get("name"),
                "tag": tag.name,
                "text": tag.text.strip()
            })

        # Extract BUTTONS
        for tag in soup.find_all("button"):
            selectors.append({
                "type": "button",
                "value": tag.text.strip(),
                "tag": "button"
            })

        return selectors

    def generate_script(self, selected_test_case_json, llm):
        test_case = json.loads(selected_test_case_json)

        html, soup = self.load_html()
        selectors = self.extract_selectors(soup)

        context = "\n".join([json.dumps(s, indent=2) for s in selectors])

        prompt = f"""
You are a senior QA Automation Engineer who writes perfect Selenium Python scripts.

STRICT RULES:
- Use ONLY selectors available in the provided checkout HTML structure.
- Do NOT invent HTML IDs or names.
- Prefer:
    driver.find_element(By.ID, ...)
    driver.find_element(By.NAME, ...)
    driver.find_element(By.CSS_SELECTOR, ...)
- Code must be runnable with:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
- Include waits (implicitly_wait).
- Include comments.
- Use correct steps from the test case.
- No placeholder selectors.

=== TEST CASE ===
{json.dumps(test_case, indent=2)}

=== AVAILABLE HTML SELECTORS (REAL EXTRACTED) ===
{context}

=== NOW GENERATE THE FINAL SELENIUM PYTHON SCRIPT ===
Return only the code inside a Python code block.
"""

        return llm(prompt)
