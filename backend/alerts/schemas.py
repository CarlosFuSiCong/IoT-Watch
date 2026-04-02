from datetime import datetime
from pydantic import BaseModel
from alerts.models import AlertType


class AlertResponse(BaseModel):
    id: int
    device_id: str
    type: AlertType
    message: str
    timestamp: datetime

    model_config = {"from_attributes": True}


class AlertPage(BaseModel):
    items: list[AlertResponse]
    total: int
    page: int
    limit: int
