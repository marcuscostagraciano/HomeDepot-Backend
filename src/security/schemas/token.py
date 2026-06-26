from core.schemas import BaseSchema


class TokenSchema(BaseSchema):
    access_token: str
    token_type: str
