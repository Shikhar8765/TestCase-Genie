import chromadb
from langchain.embeddings.huggingface import HuggingFaceEmbeddings

class VectorEngine:
    def __init__(self, vector_db_path="backend/storage/vector_db"):
        self.client = chromadb.PersistentClient(path=vector_db_path)

        # Try to load collection, else create it
        try:
            self.collection = self.client.get_collection("qa_knowledge_base")
        except:
            self.collection = self.client.create_collection("qa_knowledge_base")

        self.embedder = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )

    def search(self, query, k=5):
        query_embedding = self.embedder.embed_query(query)

        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=k
        )

        documents = results["documents"][0]
        metadatas = results["metadatas"][0]

        return list(zip(documents, metadatas))
