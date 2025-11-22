# ---- Base Image ----
FROM python:3.10-slim

# ---- Set Work Directory ----
WORKDIR /app

# ---- Install System Dependencies ----
RUN apt-get update && apt-get install -y \
    build-essential \
    chromium-driver \
    chromium \
    curl \
    && apt-get clean

# ---- Copy Project Files ----
COPY . /app

# ---- Install Python Dependencies ----
RUN pip install --no-cache-dir -r requirements.txt

# ---- Expose Ports ----
EXPOSE 7860
EXPOSE 7861

# ---- Run Backend + Streamlit Together ----
CMD ["bash", "-c", "uvicorn backend.main:app --host 0.0.0.0 --port 7860 & streamlit run frontend/app.py --server.port 7861 --server.address 0.0.0.0"]
