from typing import Protocol


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
