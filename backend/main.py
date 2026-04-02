import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

import mqtt

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s — %(message)s",
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    mqtt.start()
    yield
    mqtt.stop()


app = FastAPI(title="IoT Watch API", version="0.1.0", lifespan=lifespan)


@app.get("/health")
def health():
    return {"status": "ok"}
