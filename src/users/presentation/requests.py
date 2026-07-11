from pydantic import EmailStr

from core.presentation.requests import BaseRequestPresentation


class UserCreateRequestPresentation(BaseRequestPresentation):
    first_name: str
    last_name: str
    password: str
    email: EmailStr
