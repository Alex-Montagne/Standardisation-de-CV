FROM python:3.10-slim

RUN apt-get update && \
    apt-get install -y tesseract-ocr tesseract-ocr-fra tesseract-ocr-eng && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]