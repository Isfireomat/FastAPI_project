FROM python:3.11.5-slim

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY . . 

RUN pip install poetry && \
    poetry install
    

EXPOSE 8000

CMD poetry run uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload