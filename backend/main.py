import asyncio
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

import mqtt
from devices.service import offline_checker

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s — %(message)s",
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    mqtt.start()
    task = asyncio.create_task(offline_checker())
    yield
    task.cancel()
    mqtt.stop()


app = FastAPI(title="IoT Watch API", version="0.1.0", lifespan=lifespan)


@app.get("/health")
def health():
    return {"status": "ok"}
