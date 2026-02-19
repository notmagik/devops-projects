import os
import time
import psycopg
from fastapi import FastAPI

DB_DSN = os.getenv("DB_DSN", "postgresql://app:app@db:5432/appdb")

app = FastAPI()

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/db")
def db_check():
    t0 = time.time()
    with psycopg.connect(DB_DSN) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT 1;")
            val = cur.fetchone()[0]
    return {"db": "ok", "select": val, "latency_ms": int((time.time()-t0)*1000)}

@app.get("/ready")
def ready():
    try:
        with psycopg.connect(DB_DSN) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT 1;")
        return {"status": "ready"}
    except Exception:
        return {"status": "not ready"}
