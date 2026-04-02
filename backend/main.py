import asyncio
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

import mqtt
from devices.service import offline_checker
from devices.router import router as devices_router
from telemetry.router import router as telemetry_router
from alerts.router import router as alerts_router
from demo.router import router as demo_router

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
    await asyncio.gather(task, return_exceptions=True)
    mqtt.stop()


app = FastAPI(title="IoT Watch API", version="0.1.0", lifespan=lifespan)

app.include_router(devices_router)
app.include_router(telemetry_router)
app.include_router(alerts_router)
app.include_router(demo_router)


@app.get("/health")
def health():
    return {"status": "ok"}