FROM python:3.10-slim

WORKDIR /app

# Install minimal OS dependencies (Streamlit + FastAPI don't need chromium)
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && apt-get clean

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

# Render exposes PORT env automatically
ENV PORT=10000

EXPOSE 10000

CMD ["python", "app.py"]
