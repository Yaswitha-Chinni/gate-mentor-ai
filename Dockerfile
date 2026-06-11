FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Expose the port Cloud Run uses
EXPOSE 8080

# Command to run FastAPI
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8080"]
