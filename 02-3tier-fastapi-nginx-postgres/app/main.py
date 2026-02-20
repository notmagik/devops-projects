import os
import time

import psycopg
from fastapi import FastAPI, Response
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST

DB_DSN = os.getenv("DB_DSN", "postgresql://app:app@db:5432/appdb")

app = FastAPI()

# Metrics:
# - http_requests_total: total number of requests hitting our endpoints
# - http_request_duration_seconds: request latency distribution (histogram)
REQUEST_COUNT = Counter(
    "http_requests_total",
    "Total number of HTTP requests to the application endpoints",
)

REQUEST_LATENCY = Histogram(
    "http_request_duration_seconds",
    "HTTP request duration in seconds",
)


@app.get("/health")
def health():
    REQUEST_COUNT.inc()
    with REQUEST_LATENCY.time():
        return {"status": "ok"}


@app.get("/ready")
def ready():
    REQUEST_COUNT.inc()
    with REQUEST_LATENCY.time():
        try:
            with psycopg.connect(DB_DSN) as conn:
                with conn.cursor() as cur:
                    cur.execute("SELECT 1;")
            return {"status": "ready"}
        except Exception:
            return {"status": "not ready"}


@app.get("/db")
def db_check():
    REQUEST_COUNT.inc()
    with REQUEST_LATENCY.time():
        t0 = time.time()
        with psycopg.connect(DB_DSN) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT 1;")
                val = cur.fetchone()[0]
        return {"db": "ok", "select": val, "latency_ms": int((time.time() - t0) * 1000)}


@app.get("/metrics")
def metrics():
    # Prometheus expects a text-based exposition format, not JSON.
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)
