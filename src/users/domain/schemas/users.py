from dataclasses import dataclass
from uuid import UUID

from core.domain.errors import InvalidFieldError, RequiredFieldMissingError
from core.domain.schemas import DomainCreateSchema, DomainReadSchema, DomainSchema


@dataclass(frozen=True)
class User(DomainSchema):
    first_name: str
    last_name: str
    email: str


@dataclass(frozen=True)
class UserCreate(User, DomainCreateSchema):
    password: str

    def __post_init__(self):
        if not self.first_name:
            raise RequiredFieldMissingError("first_name")
        if not self.last_name:
            raise RequiredFieldMissingError("last_name")
        if not self.email:
            raise RequiredFieldMissingError("email")
        if not self.password:
            raise RequiredFieldMissingError("password")
        if len(self.password) < 8:
            raise InvalidFieldError(
                message="Password must be at least 8 characters long"
            )


@dataclass(frozen=True)
class UserRead(User, DomainReadSchema):
    id: UUID
    password: str


@dataclass(frozen=True)
class UserUpdate(DomainSchema):
    first_name: str | None = None
    last_name: str | None = None
    email: str | None = None
    password: str | None = None
