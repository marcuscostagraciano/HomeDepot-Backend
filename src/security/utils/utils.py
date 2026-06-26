from datetime import datetime, timedelta
from typing import Any, Dict
from zoneinfo import ZoneInfo

from jwt import decode, encode
from pwdlib import PasswordHash

from core.utils import get_dotenv_config
from security.schemas.token import TokenSchema

password_hash = PasswordHash.recommended()


def generate_hash(password: str) -> str:
    """Hashed password.

    Args:
        password (str): Password to hash.

    Returns:
        str: Hashed password.
    """
    return password_hash.hash(password)


def validate_hash(password: str, hashed_password: str) -> bool:
    """Validate if the plain password is the same as the hashed password.

    Args:
        password (str): Plain password.
        hashed_password (str): Hashed version of the password.

    Returns:
        bool: `True` if the hashed `password` equals the `hashed_password`, `False` otherwise.
    """
    return password_hash.verify(password, hashed_password)


def generate_jwt_token(payload: Dict[str, Any]) -> TokenSchema:
    """Generates a JWT token.

    Args:
        payload (dict): Payload to encode in the JWT token.

    Returns:
        TokenSchema: Encoded JWT token.
    """

    return_payload: Dict[str, Any] = payload.copy()
    return_payload.update(
        {
            "exp": datetime.now(tz=ZoneInfo("UTC"))
            + timedelta(
                minutes=int(get_dotenv_config(config_key="ACCESS_TOKEN_EXPIRE_MINUTES"))
            )
        }
    )

    return TokenSchema(
        token_type="Bearer",
        access_token=encode(
            payload=return_payload,
            key=get_dotenv_config("JWT_SECRET"),
            algorithm=get_dotenv_config("JWT_ALGORITHM"),
        ),
    )


def decode_jwt_token(token: str) -> Dict[str, Any]:
    """Decodes a JWT token.

    Args:
        token (str): JWT token to decode.

    Returns:
        dict: Decoded payload from the JWT token.
    """
    return decode(
        jwt=token,
        key=get_dotenv_config("JWT_SECRET"),
        algorithms=[get_dotenv_config("JWT_ALGORITHM")],
    )
