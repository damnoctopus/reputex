"""Centralized application exception definitions and error handlers."""

from typing import Any

from fastapi import HTTPException, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse


class AppException(HTTPException):
    """Base application exception with structured error payload."""

    def __init__(
        self,
        status_code: int,
        code: str,
        message: str,
        details: dict[str, Any] | None = None,
    ):
        super().__init__(status_code=status_code, detail=message)
        self.code = code
        self.message = message
        self.details = details or {}


class NotFoundException(AppException):
    def __init__(
        self, message: str = "Resource not found", code: str = "NOT_FOUND", details: dict[str, Any] | None = None
    ):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, code=code, message=message, details=details)


class BadRequestException(AppException):
    def __init__(self, message: str = "Bad request", code: str = "BAD_REQUEST", details: dict[str, Any] | None = None):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, code=code, message=message, details=details)


class UnauthorizedException(AppException):
    def __init__(
        self, message: str = "Authentication failed", code: str = "UNAUTHORIZED", details: dict[str, Any] | None = None
    ):
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, code=code, message=message, details=details)


class ForbiddenException(AppException):
    def __init__(self, message: str = "Access denied", code: str = "FORBIDDEN", details: dict[str, Any] | None = None):
        super().__init__(status_code=status.HTTP_403_FORBIDDEN, code=code, message=message, details=details)


class ConflictException(AppException):
    def __init__(
        self, message: str = "Resource conflict", code: str = "CONFLICT", details: dict[str, Any] | None = None
    ):
        super().__init__(status_code=status.HTTP_409_CONFLICT, code=code, message=message, details=details)


def build_error_response(
    status_code: int, code: str, message: str, details: dict[str, Any] | None = None
) -> JSONResponse:
    """Builds a standardized error JSON response compatible with Flutter and API contracts."""
    content = {
        "success": False,
        "detail": message,
        "message": message,
        "error": {
            "code": code,
            "message": message,
            "details": details or {},
        },
    }
    return JSONResponse(status_code=status_code, content=content)


async def app_exception_handler(request: Request, exc: AppException) -> JSONResponse:
    return build_error_response(
        status_code=exc.status_code,
        code=exc.code,
        message=exc.message,
        details=exc.details,
    )


async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    errors = exc.errors()
    first_msg = errors[0]["msg"] if errors else "Invalid data provided"
    return build_error_response(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        code="VALIDATION_ERROR",
        message=first_msg,
        details={"errors": errors},
    )


async def global_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    return build_error_response(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        code="INTERNAL_SERVER_ERROR",
        message="An unexpected server error occurred. Please try again later.",
    )
