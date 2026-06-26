from security.adapters import PasswordHasher, get_password_hasher
from security.domain import PasswordHasherPort


def test_hash_does_not_return_plain_password(
    password_hasher: PasswordHasherPort,
) -> None:
    password = "batatinha123"

    hashed = password_hasher.hash(password)

    assert hashed != password


def test_verify_returns_true_for_correct_password(
    password_hasher: PasswordHasherPort,
) -> None:
    password = "batatinha123"
    hashed = password_hasher.hash(password)

    assert password_hasher.verify(password, hashed)


def test_verify_returns_false_for_wrong_password(
    password_hasher: PasswordHasherPort,
) -> None:
    hashed = password_hasher.hash("batatinha123")

    assert not password_hasher.verify("senha_errada", hashed)


def test_get_password_hasher_returns_password_hasher() -> None:
    assert isinstance(get_password_hasher(), PasswordHasher)
