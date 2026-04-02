from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from database import get_db
from devices.repository import get_device
from telemetry.repository import list_telemetry
from telemetry.schemas import SensorDataResponse, TelemetryPage
from schemas import ApiResponse

router = APIRouter(prefix="/devices", tags=["telemetry"])


@router.get("/{device_id}/telemetry", response_model=ApiResponse[TelemetryPage])
def get_telemetry(
    device_id: str,
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=50, ge=1, le=200),
    db: Session = Depends(get_db),
):
    if get_device(db, device_id) is None:
        raise HTTPException(status_code=404, detail="Device not found")

    items, total = list_telemetry(db, device_id, page, limit)
    return ApiResponse.ok(
        TelemetryPage(
            items=[SensorDataResponse.model_validate(r) for r in items],
            total=total,
            page=page,
            limit=limit,
        )
    )
