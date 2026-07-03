from dataclasses import dataclass

from core.domain.schemas import DomainSchema


@dataclass(frozen=True)
class TokenSchema(DomainSchema):
    token_type: str
    access_token: str
