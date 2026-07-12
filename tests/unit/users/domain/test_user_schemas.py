import pytest

from core.domain.errors import InvalidFieldError, RequiredFieldMissingError
from users.domain.schemas.users import UserCreate


def test_user_create_valid() -> None:
    user = UserCreate(
        first_name="John",
        last_name="Doe",
        email="john@test.com",
        password="12345678",
    )
    assert user.first_name == "John"
    assert user.password == "12345678"


def test_user_create_missing_first_name() -> None:
    with pytest.raises(RequiredFieldMissingError, match="first_name"):
        UserCreate(
            first_name="",
            last_name="Doe",
            email="john@test.com",
            password="12345678",
        )


def test_user_create_missing_last_name() -> None:
    with pytest.raises(RequiredFieldMissingError, match="last_name"):
        UserCreate(
            first_name="John",
            last_name="",
            email="john@test.com",
            password="12345678",
        )


def test_user_create_missing_email() -> None:
    with pytest.raises(RequiredFieldMissingError, match="email"):
        UserCreate(
            first_name="John",
            last_name="Doe",
            email="",
            password="12345678",
        )


def test_user_create_missing_password() -> None:
    with pytest.raises(RequiredFieldMissingError, match="password"):
        UserCreate(
            first_name="John",
            last_name="Doe",
            email="john@test.com",
            password="",
        )


def test_user_create_short_password() -> None:
    with pytest.raises(InvalidFieldError, match="at least 8"):
        UserCreate(
            first_name="John",
            last_name="Doe",
            email="john@test.com",
            password="1234567",
        )


def test_user_create_frozen() -> None:
    user = UserCreate(
        first_name="John",
        last_name="Doe",
        email="john@test.com",
        password="12345678",
    )
    with pytest.raises(Exception):
        user.first_name = "Jane"  # type: ignore
