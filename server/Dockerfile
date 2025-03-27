FROM python:3.9-slim
RUN apt-get update && apt-get install -y netcat-openbsd && rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY server.py .
CMD ["python", "-u", "server.py"]