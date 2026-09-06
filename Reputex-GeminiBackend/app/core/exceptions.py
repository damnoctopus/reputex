"""Normalized exception classes matching Flutter error handler schema."""
from typing import Any, Dict, Optional
from fastapi import HTTPException, status


class ReputexException(HTTPException):
    def __init__(
        self,
        status_code: int = status.HTTP_400_BAD_REQUEST,
        message: str = "An error occurred",
        code: str = "INTERNAL_ERROR",
        detail: Optional[str] = None,
        extra: Optional[Dict[str, Any]] = None,
    ):
        self.message = message
        self.code = code
        self.extra = extra or {}
        error_payload = {
            "code": code,
            "message": message,
            "detail": detail or message,
            **self.extra,
        }
        super().__init__(status_code=status_code, detail=error_payload)


class NotFoundError(ReputexException):
    def __init__(self, resource: str, resource_id: Any):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            message=f"{resource} with id '{resource_id}' was not found",
            code="NOT_FOUND",
        )


class AuthenticationError(ReputexException):
    def __init__(self, message: str = "Invalid credentials or token expired"):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            message=message,
            code="UNAUTHORIZED",
        )


class ConflictError(ReputexException):
    def __init__(self, message: str):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            message=message,
            code="CONFLICT",
        )
