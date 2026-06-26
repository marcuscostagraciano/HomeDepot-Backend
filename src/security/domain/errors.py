from http import HTTPStatus

from core.errors import BaseError


class UnauthorizedError(BaseError):
    """Exception raised for invalid authentication credentials."""

    http_status_code: HTTPStatus = HTTPStatus.UNAUTHORIZED

    def __init__(self, message: str = "Unauthorized"):
        super().__init__(message)
