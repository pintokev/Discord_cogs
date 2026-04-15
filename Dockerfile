FROM python:3.11-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    GPT_BASE_URL=http://gpt:8080 \
    GEMINI_BASE_URL=http://gemini:8080

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt
RUN apt-get update && \
    apt-get install -y --no-install-recommends curl && \
    rm -rf /var/lib/apt/lists/*
COPY src ./src

RUN useradd -m -u 10001 appuser && \
    chown -R appuser:appuser /app

USER appuser

CMD ["python", "-m", "src.discordhandler"]
