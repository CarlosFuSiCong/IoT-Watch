from typing import Any, Generic, TypeVar
from pydantic import BaseModel

T = TypeVar("T")


class ApiResponse(BaseModel, Generic[T]):
    success: bool
    data: T | None = None
    message: str | None = None

    @classmethod
    def ok(cls, data: Any) -> "ApiResponse":
        return cls(success=True, data=data)

    @classmethod
    def error(cls, message: str) -> "ApiResponse":
        return cls(success=False, message=message)
