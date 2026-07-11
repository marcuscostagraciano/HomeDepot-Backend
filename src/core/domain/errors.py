from http import HTTPStatus


class BaseError(Exception):
    """Base class for all custom exceptions in the application."""

    http_status_code: HTTPStatus

    def __init__(self, message: str):
        self.message = message
        super().__init__(message)


class InvalidFieldError(BaseError):
    """Exception raised when a field in the input data is invalid."""

    http_status_code = HTTPStatus.UNPROCESSABLE_CONTENT

    def __init__(self, field_name: str | None = None, message: str | None = None):
        self.field_name = field_name
        super().__init__(
            message or f"The field '{field_name}' is invalid.",
        )


class RequiredFieldMissingError(BaseError):
    """Exception raised when a required field is missing in the input data."""

    http_status_code = HTTPStatus.BAD_REQUEST

    def __init__(self, field_name: str):
        self.field_name = field_name
        super().__init__(
            f"The required field '{field_name}' is missing.",
        )


class NotNegativeNumberError(BaseError):
    """Exception raised when a number is expected to be non-negative but is negative."""

    http_status_code = HTTPStatus.BAD_REQUEST

    def __init__(self, field_name: str, value: float):
        self.field_name = field_name
        self.value = value
        super().__init__(
            f"The field '{field_name}' must be a non-negative number. Received: {value}",
        )


class NotFoundError(BaseError):
    """Exception raised when a requested resource is not found."""

    http_status_code: HTTPStatus = HTTPStatus.NOT_FOUND

    def __init__(self, resource_name: str, identifier: str):
        self.resource_name = resource_name
        self.identifier = identifier
        super().__init__(
            f"{resource_name} with identifier '{identifier}' was not found.",
        )


class GreaterEqualError(BaseError):
    """Exception raised when a field is not greater or equal the defined value."""

    http_status_code = HTTPStatus.BAD_REQUEST

    def __init__(
        self,
        field_name: str,
        value: int,
    ):
        self.field_name = field_name
        super().__init__(
            f"The '{field_name}' field must be greater or equal to: '{value}'",
        )


class OutsideLimitError(BaseError):
    """Exception raised when a required field is missing in the input data."""

    http_status_code = HTTPStatus.BAD_REQUEST

    def __init__(
        self,
        field_name: str,
        lower_value: int,
        upper_value: int,
    ):
        self.field_name = field_name
        super().__init__(
            f"The '{field_name}' field must be between: '{lower_value}' and '{upper_value}'",
        )


class UnauthorizedError(BaseError):
    """Exception raised for invalid authentication credentials."""

    http_status_code: HTTPStatus = HTTPStatus.UNAUTHORIZED

    def __init__(self, message: str = "Unauthorized"):
        super().__init__(message)


class ForbiddenError(BaseError):
    """Exception raised when the provided credentials are invalid."""

    http_status_code: HTTPStatus = HTTPStatus.FORBIDDEN

    def __init__(self, message: str = "Access forbidden"):
        super().__init__(message)


class ExpiredTokenError(UnauthorizedError):
    """Exception raised when the provided token has expired."""

    def __init__(self, message: str = "Expired token"):
        super().__init__(message)
