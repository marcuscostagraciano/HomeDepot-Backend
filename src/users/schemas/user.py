from core.schemas.base import BaseCreateSchema, BaseReadSchema


class User(BaseCreateSchema):
    first_name: str
    last_name: str
    email: str


class UserCreate(User):
    password: str


class UserRead(User, BaseReadSchema):
    pass


class UserUpdate(BaseCreateSchema):
    first_name: str | None = None
    last_name: str | None = None
    email: str | None = None
    password: str | None = None
