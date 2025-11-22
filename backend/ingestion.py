import os
import json
import fitz  # PyMuPDF
from bs4 import BeautifulSoup
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.embeddings.huggingface import HuggingFaceEmbeddings
import chromadb

class DocumentIngestion:

    def __init__(self, vector_db_path="backend/storage/vector_db"):
        self.client = chromadb.PersistentClient(path=vector_db_path)
        self.collection = self.client.get_or_create_collection(
            name="qa_knowledge_base",
            metadata={"hnsw:space": "cosine"}
        )
        self.embedder = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

    # ----------------------------
    # 1. PARSE PDF / TXT / MD FILES
    # ----------------------------
    def parse_document(self, file_path):
        ext = file_path.split(".")[-1].lower()

        if ext == "pdf":
            return self._parse_pdf(file_path)
        elif ext in ["txt", "md"]:
            return self._parse_text(file_path)
        elif ext == "json":
            return self._parse_json(file_path)
        else:
            return ""

    def _parse_pdf(self, path):
        text = ""
        doc = fitz.open(path)
        for page in doc:
            text += page.get_text()
        return text

    def _parse_text(self, path):
        with open(path, "r", encoding="utf-8") as f:
            return f.read()

    def _parse_json(self, path):
        with open(path, "r", encoding="utf-8") as f:
            return json.dumps(json.load(f), indent=2)

    # ----------------------------
    # 2. PARSE checkout.html
    # ----------------------------
    def parse_html(self, html_path):
        with open(html_path, "r", encoding="utf-8") as f:
            html = f.read()

        soup = BeautifulSoup(html, "html.parser")

        readable_text = soup.get_text(separator="\n")
        return readable_text, str(soup)

    # ----------------------------
    # 3. CHUNK + EMBED + STORE
    # ----------------------------
    def build_knowledge_base(self, files):
        """
        files = list of (file_path, source_name)
        """

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=800,
            chunk_overlap=100
        )

        for file_path, source_name in files:
            print(f"Ingesting {source_name}...")

            if source_name.endswith(".html"):
                raw_text, full_html = self.parse_html(file_path)

                chunks = text_splitter.split_text(raw_text)

                for i, chunk in enumerate(chunks):
                    embedding = self.embedder.embed_query(chunk)
                    self.collection.add(
                        ids=[f"{source_name}-{i}"],
                        documents=[chunk],
                        metadatas=[{"source": source_name, "type": "html"}],
                        embeddings=[embedding]
                    )

            else:
                raw_text = self.parse_document(file_path)

                chunks = text_splitter.split_text(raw_text)

                for i, chunk in enumerate(chunks):
                    embedding = self.embedder.embed_query(chunk)
                    self.collection.add(
                        ids=[f"{source_name}-{i}"],
                        documents=[chunk],
                        metadatas=[{"source": source_name}],
                        embeddings=[embedding]
                    )

        return "Knowledge Base Built Successfully!"
