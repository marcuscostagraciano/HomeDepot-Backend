from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from ..adapters import get_jwt_service
from ..domain import AuthRepositoryPort, JWTServicePort
from ..domain import get_token as get_token_use_case
from ..repositories import get_auth_repository
from ..schemas.token import TokenSchema

router = APIRouter(prefix="/token", tags=["token"])


@router.post("/")
async def get_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    repository: AuthRepositoryPort = Depends(get_auth_repository),
    jwt_service: JWTServicePort = Depends(get_jwt_service),
) -> TokenSchema:
    return await get_token_use_case(
        username=form_data.username,
        password=form_data.password,
        repository=repository,
        jwt_service=jwt_service,
    )
