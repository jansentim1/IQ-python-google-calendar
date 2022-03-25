FROM python:3.8.5-slim

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["gunicorn", "main:app", "--workers", "1", "--worker-class", "uvicorn.workers.UvicornWorker", "--log-level=warning", "--access-logfile", "-", "--error-logfile", "-", "--timeout", "6000", "-b", ":8001"]
