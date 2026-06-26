from typing import Any, Dict

from security.adapters import JWTService, get_jwt_service
from security.domain import JWTServicePort
from security.schemas import TokenSchema


def test_generate_returns_token_schema(
    jwt_service: JWTServicePort,
    payload: Dict[str, Any],
) -> None:
    generated: TokenSchema = jwt_service.generate(payload)
    assert isinstance(generated, TokenSchema)


def test_generate_does_not_mutate_payload(
    jwt_service: JWTServicePort,
    payload: Dict[str, Any],
) -> None:
    jwt_service.generate(payload)

    assert "exp" not in payload


def test_decode_returns_original_payload(
    jwt_service: JWTServicePort,
    payload: Dict[str, Any],
) -> None:
    generated = jwt_service.generate(payload)

    decoded = jwt_service.decode(generated.access_token)

    assert decoded["email"] == payload["email"]


def test_generate_adds_expiration_claim(
    jwt_service: JWTServicePort,
    payload: Dict[str, Any],
) -> None:
    generated = jwt_service.generate(payload)

    decoded = jwt_service.decode(generated.access_token)

    assert "exp" in decoded


def test_get_jwt_service_returns_jwt_service() -> None:
    assert isinstance(get_jwt_service(), JWTService)
