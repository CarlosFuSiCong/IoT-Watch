from datetime import datetime
from pydantic import BaseModel


class SensorDataResponse(BaseModel):
    id: int
    device_id: str
    temperature: float
    humidity: float
    battery: float
    timestamp: datetime

    model_config = {"from_attributes": True}


class TelemetryPage(BaseModel):
    items: list[SensorDataResponse]
    total: int
    page: int
    limit: int
