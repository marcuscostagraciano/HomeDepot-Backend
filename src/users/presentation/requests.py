from pydantic import EmailStr, SecretStr

from core.presentation.requests import BaseRequestPresentation


class UserCreateRequestPresentation(BaseRequestPresentation):
    first_name: str
    last_name: str
    password: SecretStr
    email: EmailStr
