import pytest

from users.domain.errors import UniqueEmailError


def test_unique_email_error_default_message() -> None:
    error = UniqueEmailError()
    assert error.message == "Email already exists"


def test_unique_email_error_custom_message() -> None:
    error = UniqueEmailError("custom message")
    assert error.message == "custom message"


def test_unique_email_error_http_status() -> None:
    from http import HTTPStatus

    error = UniqueEmailError()
    assert error.http_status_code == HTTPStatus.CONFLICT
