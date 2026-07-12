from http import HTTPStatus

import pytest

from core.domain.errors import (
    BaseError,
    ExpiredTokenError,
    ForbiddenError,
    GreaterEqualError,
    InvalidFieldError,
    NotFoundError,
    NotNegativeNumberError,
    OutsideLimitError,
    RequiredFieldMissingError,
    UnauthorizedError,
)


@pytest.mark.parametrize(
    "error_class,args,expected_status,message_contains",
    [
        (
            InvalidFieldError,
            ("email", "invalid"),
            HTTPStatus.UNPROCESSABLE_CONTENT,
            "invalid",
        ),
        (RequiredFieldMissingError, ("name",), HTTPStatus.BAD_REQUEST, "missing"),
        (NotFoundError, ("User", "123"), HTTPStatus.NOT_FOUND, "not found"),
        (GreaterEqualError, ("page", 1), HTTPStatus.BAD_REQUEST, "greater or equal"),
        (OutsideLimitError, ("limit", 1, 100), HTTPStatus.BAD_REQUEST, "between"),
        (UnauthorizedError, (), HTTPStatus.UNAUTHORIZED, "Unauthorized"),
        (ForbiddenError, (), HTTPStatus.FORBIDDEN, "Access forbidden"),
        (ExpiredTokenError, (), HTTPStatus.UNAUTHORIZED, "Expired token"),
        (
            NotNegativeNumberError,
            ("price", -1.0),
            HTTPStatus.BAD_REQUEST,
            "non-negative",
        ),
    ],
)
def test_error_classes_set_http_status_and_message(
    error_class,
    args,
    expected_status,
    message_contains,
) -> None:
    error = error_class(*args)

    assert isinstance(error, BaseError)
    assert error.http_status_code == expected_status
    assert message_contains in error.message


def test_invalid_field_error_without_field_name() -> None:
    error = InvalidFieldError(message="custom error")
    assert error.field_name is None
    assert error.message == "custom error"


def test_base_error_is_exception() -> None:
    error = BaseError("failure")

    assert isinstance(error, Exception)
    assert error.message == "failure"
