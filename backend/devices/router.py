from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from devices.repository import get_device, list_devices
from devices.schemas import DeviceResponse
from schemas import ApiResponse

router = APIRouter(prefix="/devices", tags=["devices"])


@router.get("", response_model=ApiResponse[list[DeviceResponse]])
def get_devices(db: Session = Depends(get_db)):
    devices = list_devices(db)
    return ApiResponse.ok([DeviceResponse.model_validate(d) for d in devices])


@router.get("/{device_id}", response_model=ApiResponse[DeviceResponse])
def get_device_by_id(device_id: str, db: Session = Depends(get_db)):
    device = get_device(db, device_id)
    if device is None:
        raise HTTPException(status_code=404, detail="Device not found")
    return ApiResponse.ok(DeviceResponse.model_validate(device))
