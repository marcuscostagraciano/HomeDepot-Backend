from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

import core.domain as errors
from db.db import get_async_session
from users.adapters import get_current_user

from ..domain import use_cases
from ..repositories.list_repository import ListRepository
from ..schemas.list import ListCreate, ListRead

router = APIRouter(
    prefix="/lists", tags=["lists"], dependencies=[Depends(get_async_session)]
)


@router.post("/", response_model=ListRead)
async def create_list(
    list_create: ListCreate,
    session: AsyncSession = Depends(get_async_session),
):
    try:
        repository = ListRepository(session)
        created = await use_cases.create_list(list_create, repository)
    except errors.BaseError as e:
        raise HTTPException(status_code=e.http_status_code, detail=str(e))

    return created


@router.get("/{list_id}", response_model=ListRead)
async def read_list(
    list_id: UUID, session: AsyncSession = Depends(get_async_session)
) -> ListRead:
    try:
        repository = ListRepository(session)
        list_obj = await use_cases.read_list(list_id, repository)
    except errors.NotFoundError as e:
        raise HTTPException(status_code=e.http_status_code, detail=str(e))

    return list_obj


@router.delete("/{list_id}", response_model=ListRead)
async def delete_list(
    list_id: UUID, session: AsyncSession = Depends(get_async_session)
):
    try:
        repository = ListRepository(session)
        result = await use_cases.delete_list(list_id, repository)
    except errors.BaseError as e:
        raise HTTPException(status_code=e.http_status_code, detail=str(e))

    return result
