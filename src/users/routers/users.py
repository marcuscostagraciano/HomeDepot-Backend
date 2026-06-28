from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

import core.domain as errors
from db.db import get_async_session
from security.adapters import get_password_hasher
from security.domain import PasswordHasherPort

from ..domain import use_cases
from ..repositories.user_repository import UserRepository
from ..schemas.user import UserCreate, UserRead

router = APIRouter(
    prefix="/users", tags=["users"], dependencies=[Depends(get_async_session)]
)


@router.post("/", response_model=UserRead)
async def create_user(
    payload: UserCreate,
    session: AsyncSession = Depends(get_async_session),
) -> UserRead:
    try:
        repository = UserRepository(session)
        user = await use_cases.create_user(payload, repository)
    except errors.BaseError as e:
        raise HTTPException(status_code=e.http_status_code, detail=str(e))

    return user


@router.get("/{id}", response_model=UserRead)
async def read_user(
    id: UUID,
    session: AsyncSession = Depends(get_async_session),
) -> UserRead | None:
    try:
        repository = UserRepository(session)
        user = await use_cases.read_user(id, repository)
    except errors.NotFoundError as e:
        raise HTTPException(status_code=e.http_status_code, detail=str(e))

    return user
