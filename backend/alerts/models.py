import enum
from datetime import datetime, timezone
from sqlalchemy import String, Text, DateTime, Enum as SAEnum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from database import Base


class AlertType(str, enum.Enum):
    HIGH_TEMPERATURE = "HIGH_TEMPERATURE"
    LOW_BATTERY = "LOW_BATTERY"
    OFFLINE = "OFFLINE"


class Alert(Base):
    __tablename__ = "alerts"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    # string FK avoids importing Device class directly
    device_id: Mapped[str] = mapped_column(
        String(64), ForeignKey("devices.id"), nullable=False
    )
    type: Mapped[AlertType] = mapped_column(
        SAEnum(AlertType, name="alerttype"), nullable=False
    )
    message: Mapped[str] = mapped_column(Text, nullable=False)
    timestamp: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
