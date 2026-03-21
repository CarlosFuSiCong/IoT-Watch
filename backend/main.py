# IoT Watch Backend — FastAPI entry
from fastapi import FastAPI

app = FastAPI(title="IoT Watch API", version="0.1.0")


@app.get("/health")
def health():
    return {"status": "ok"}
