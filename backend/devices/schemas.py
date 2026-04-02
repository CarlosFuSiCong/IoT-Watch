from datetime import datetime
from pydantic import BaseModel
from devices.models import DeviceStatus


class DeviceResponse(BaseModel):
    id: str
    name: str
    status: DeviceStatus
    last_seen: datetime | None
    created_at: datetime

    model_config = {"from_attributes": True}
