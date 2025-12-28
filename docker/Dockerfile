FROM python:3.10-slim

WORKDIR /app

RUN apt-get update && apt-get install -y build-essential libmagic1 && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml README.md .
RUN pip install --upgrade pip && pip install .

COPY . .

CMD ["uvicorn", "src.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
