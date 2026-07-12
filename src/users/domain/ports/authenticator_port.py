from typing import Any, Dict, Protocol

from ..schemas import TokenSchema, UserRead


class AuthenticatorPort(Protocol):
    async def authenticate(self, email: str, password: str) -> UserRead | None: ...


class JWTServicePort(Protocol):
    def generate(self, payload: Dict[str, Any]) -> TokenSchema:
        """Generates a JWT token.

        Args:
            payload (dict): Payload to encode in the JWT token.

        Returns:
            TokenSchema: Encoded JWT token.
        """
        ...

    def decode(self, token: str) -> Dict[str, Any]:
        """Decodes a JWT token.

        Args:
            token (str): JWT token to decode.

        Returns:
            dict: Decoded payload from the JWT token.
        """
        ...


class PasswordHasherPort(Protocol):
    def hash(self, password: str) -> str:
        """Hashed password.

        Args:
            password (str): Password to hash.

        Returns:
            str: Hashed password.
        """
        ...

    def verify(self, password: str, hashed_password: str) -> bool:
        """Validate if the plain password is the same as the hashed password.

        Args:
            password (str): Plain password.
            hashed_password (str): Hashed version of the password.

        Returns:
            bool: `True` if the hashed `password` equals the `hashed_password`, `False` otherwise.
        """
        ...
