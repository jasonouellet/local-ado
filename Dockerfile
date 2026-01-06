FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Install deps
COPY pyproject.toml /app/pyproject.toml
COPY src /app/src

RUN pip install --no-cache-dir --upgrade pip \
 && pip install --no-cache-dir .

COPY fixtures /app/fixtures

EXPOSE 8080

CMD ["python", "-m", "azure_api_mock"]
