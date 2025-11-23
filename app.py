import subprocess
import threading
import os

PORT = os.environ.get("PORT", "10000")

def run_backend():
    subprocess.run([
        "uvicorn", "backend.main:app",
        "--host", "0.0.0.0",
        "--port", PORT
    ])

def run_frontend():
    subprocess.run([
        "streamlit", "run", "frontend/app.py",
        "--server.address=0.0.0.0",
        "--server.port=" + PORT
    ])

if __name__ == "__main__":
    t1 = threading.Thread(target=run_backend)
    t2 = threading.Thread(target=run_frontend)
    t1.start()
    t2.start()
    t1.join()
    t2.join()
