# syntax=docker/dockerfile:1.7
FROM python:3.12-slim

# WeasyPrint needs these system libraries for PDF rendering.
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpango-1.0-0 libpangocairo-1.0-0 libcairo2 libgdk-pixbuf-2.0-0 \
    libffi-dev libpq5 fonts-dejavu \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
# Cache mount keeps downloaded wheels across attempts; longer timeout and
# retries tolerate slow or flaky networks.
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install --timeout 120 --retries 10 -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["./entrypoint.sh"]
