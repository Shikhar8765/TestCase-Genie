import os

# HF will run this file but Dockerfile will override runtime.
# Still required so HuggingFace stops showing "No application file"
print("🚀 TestCase-Genie backend/frontend launching via Dockerfile...")

# This script does nothing, Dockerfile actually runs uvicorn + streamlit.
