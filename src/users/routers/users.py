from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from core.presentation.dependencies import RequestContext, get_request_context
from db.db import get_async_session

from ..adapters.authenticator import get_authenticator
from ..adapters.jwt_service import get_jwt_service
from ..adapters.password_hasher import get_password_hasher
from ..domain.ports import AuthenticatorPort, JWTServicePort, PasswordHasherPort
from ..domain.schemas import TokenSchema, UserCreate
from ..domain.use_cases import create_user as create_user_case
from ..domain.use_cases import get_token as get_token_use_case
from ..domain.use_cases import read_user as read_user_case
from ..presentation.requests import UserCreateRequestPresentation as CreateRequest
from ..presentation.responses import UserReadResponsePresentation as Response
from ..repositories.user_repository import UserRepository

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/", response_model=Response)
async def create_user(
    payload: CreateRequest,
    session: AsyncSession = Depends(get_async_session),
    password_hasher: PasswordHasherPort = Depends(get_password_hasher),
) -> Response:
    created = await create_user_case(
        UserRepository(session),
        UserCreate.from_dict(payload.to_dict()),
        password_hasher,
    )

    return Response.from_dict(created.to_dict())


@router.get("/me", response_model=Response)
async def read_user(
    context: RequestContext = Depends(get_request_context),
) -> Response:
    user = await read_user_case(
        UserRepository(context.session),
        context.user.id,
    )

    return Response.from_dict(user.to_dict())


@router.post("/login", response_model=TokenSchema)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    authenticator: AuthenticatorPort = Depends(get_authenticator),
    jwt_service: JWTServicePort = Depends(get_jwt_service),
) -> TokenSchema:
    return await get_token_use_case(
        username=form_data.username,
        password=form_data.password,
        authenticator=authenticator,
        jwt_service=jwt_service,
    )
