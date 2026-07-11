from http import HTTPStatus

from core.domain.errors import BaseError


class UniqueEmailError(BaseError):
    """Exception raised when a user with the same email already exists."""

    http_status_code: HTTPStatus = HTTPStatus.CONFLICT

    def __init__(self, message: str = "Email already exists"):
        super().__init__(message)
