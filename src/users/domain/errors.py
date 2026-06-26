from http import HTTPStatus

from core.errors import BaseError


class UniqueEmailError(BaseError):
    """Exception raised when a user with the same email already exists."""

    http_status_code: HTTPStatus = HTTPStatus.CONFLICT

    def __init__(self, message: str = "Email already exists"):
        super().__init__(message)


class CredentialsError(BaseError):
    """Exception raised when the provided credentials are invalid."""

    http_status_code: HTTPStatus = HTTPStatus.UNAUTHORIZED

    def __init__(self, message: str = "Invalid credentials"):
        super().__init__(message)


class ExpiredTokenError(CredentialsError):
    """Exception raised when the provided token has expired."""

    def __init__(self, message: str = "Expired token"):
        super().__init__(message)
