FROM python:3.9.7-buster
WORKDIR /fastapi
COPY requirements.txt .
RUN pip install -r requirements.txt --no-cache-dir
COPY . .
EXPOSE 8080
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]