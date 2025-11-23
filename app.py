import subprocess
import threading

# --- Start FastAPI backend on port 7860 ---
def run_backend():
    subprocess.run(
        ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "7860"]
    )

# --- Start Streamlit frontend on port 7861 ---
def run_frontend():
    subprocess.run(
        ["streamlit", "run", "frontend/app.py", "--server.port=7861", "--server.address=0.0.0.0"]
    )

# Run both in parallel
threading.Thread(target=run_backend).start()
threading.Thread(target=run_frontend).start()
