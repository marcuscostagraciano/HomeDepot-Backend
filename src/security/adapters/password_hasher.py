from pwdlib import PasswordHash

from security.domain import PasswordHasherPort


class PasswordHasher(PasswordHasherPort):
    def __init__(self):
        self._hasher: PasswordHash = PasswordHash.recommended()

    def hash(self, password: str) -> str:
        return self._hasher.hash(password)

    def verify(self, password: str, hashed_password: str) -> bool:
        return self._hasher.verify(password, hashed_password)


def get_password_hasher() -> PasswordHasherPort:
    """Get a new instance of PasswordHasher.

    Returns:
        PasswordHasherPort: New instance of PasswordHasher.
    """
    return PasswordHasher()
