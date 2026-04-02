import enum
from datetime import datetime, timezone
from sqlalchemy import String, DateTime, Enum as SAEnum
from sqlalchemy.orm import Mapped, mapped_column
from database import Base


class DeviceStatus(str, enum.Enum):
    online = "online"
    offline = "offline"


class Device(Base):
    __tablename__ = "devices"

    # device_id comes from MQTT topic, e.g. "warehouse-01"
    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    name: Mapped[str] = mapped_column(String(128), nullable=False)
    status: Mapped[DeviceStatus] = mapped_column(
        SAEnum(DeviceStatus, name="devicestatus"),
        default=DeviceStatus.offline,
        nullable=False,
    )
    last_seen: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
