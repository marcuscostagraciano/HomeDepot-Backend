from http import HTTPStatus
from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db.db import get_async_session

from ..models.list import List as ListModel
from ..schemas import ListCreate, ListRead

router = APIRouter(
    prefix="/lists",
    tags=["lists"],
)


@router.get("/", response_model=List[ListRead])
async def read_lists(
    session: AsyncSession = Depends(get_async_session),
) -> List[ListRead]:
    result = await session.execute(select(ListModel))
    lists = result.scalars().all()
    return [ListRead.model_validate(list) for list in lists]


@router.post("/", response_model=ListRead)
async def create_list(
    list_create: ListCreate,
    session: AsyncSession = Depends(get_async_session),
):
    new_list = ListModel(**list_create.model_dump())

    session.add(new_list)
    await session.commit()
    await session.refresh(new_list)

    return ListRead.model_validate(new_list)


@router.delete("/{list_id}")
async def delete_list(
    list_id: UUID,
    session: AsyncSession = Depends(get_async_session),
):
    return {"success": True}
