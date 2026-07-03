from pydantic import EmailStr

from core.presentation.responses import BaseResponsePresentation


class UserReadResponsePresentation(BaseResponsePresentation):
    first_name: str
    last_name: str
    email: EmailStr
