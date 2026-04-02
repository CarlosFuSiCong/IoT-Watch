from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from alerts.models import AlertType
from alerts.repository import list_alerts
from alerts.schemas import AlertPage, AlertResponse
from database import get_db
from schemas import ApiResponse

router = APIRouter(prefix="/alerts", tags=["alerts"])


@router.get("", response_model=ApiResponse[AlertPage])
def get_alerts(
    device_id: str | None = Query(default=None),
    type: AlertType | None = Query(default=None),
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=50, ge=1, le=200),
    db: Session = Depends(get_db),
):
    items, total = list_alerts(db, device_id=device_id, alert_type=type, page=page, limit=limit)
    return ApiResponse.ok(
        AlertPage(
            items=[AlertResponse.model_validate(a) for a in items],
            total=total,
            page=page,
            limit=limit,
        )
    )
