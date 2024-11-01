FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["python","-m","uvicorn", "cloudPlatform.api:app", "--host", "0.0.0.0", "--port", "8000"]