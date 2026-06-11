FROM python:3.10-slim

WORKDIR /app

# Install system dependencies including ffmpeg for whisper and rust for tiktoken
RUN apt-get update && apt-get install -y \
    ffmpeg \
    build-essential \
    rustc \
    cargo \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip "setuptools<70.0.0" wheel && \
    pip install --no-cache-dir --no-build-isolation openai-whisper==20240930 && \
    pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Expose Cloud Run default port
EXPOSE 8080

# Run Streamlit
CMD ["streamlit", "run", "app.py", "--server.port=8080", "--server.address=0.0.0.0"]
