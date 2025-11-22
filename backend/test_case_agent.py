from backend.vector_engine import VectorEngine
import json

class TestCaseAgent:

    def __init__(self):
        self.retriever = VectorEngine()

    def generate_test_cases(self, feature_query, llm):
        # RAG retrieval
        context_chunks = self.retriever.search(feature_query, k=5)

        # handle case: no documents found
        if not context_chunks:
            context_text = "No relevant documents found in the knowledge base."
        else:
            context_text = "\n\n".join(
                [f"Source: {meta['source']}\n{doc}" for doc, meta in context_chunks]
            )

        prompt = f"""
You are an expert QA Test Case Generator.

STRICT RULES:
- Only use information from the provided context.
- Do not hallucinate or invent features.
- Test cases must be structured in JSON format.
- Each test case must include:
  - Test_ID
  - Feature
  - Scenario
  - Steps
  - Expected_Result
  - Grounded_In (document source)

Context:
{context_text}

User Request:
Generate comprehensive positive and negative test cases for:
"{feature_query}"

Return JSON list only.
"""

        llm_response = llm(prompt)
        return llm_response
