FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY cliente.py .
CMD ["python", "cliente.py"]