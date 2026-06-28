from http import HTTPStatus
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

import core.domain as errors
from db.db import get_async_session
from users.adapters import get_current_user

from ..adapters import get_products_filters
from ..domain import ProductFilters, use_cases
from ..repositories.product_repository import ProductRepository
from ..schemas import ProductCreate, ProductRead

router = APIRouter(
    prefix="/products",
    tags=["products"],
    dependencies=[
        # Depends(get_current_user),
    ],
)


@router.post("/", response_model=ProductRead, status_code=HTTPStatus.CREATED)
async def create_product(
    payload: ProductCreate,
    session: AsyncSession = Depends(get_async_session),
) -> ProductRead:
    try:
        repository = ProductRepository(session)
        product = await use_cases.create_product(payload, repository)
    except errors.BaseError as e:
        raise HTTPException(status_code=e.http_status_code, detail=str(e))

    return product


@router.get("/", response_model=list[ProductRead])
async def read_products(
    filters: ProductFilters = Depends(get_products_filters),
    session: AsyncSession = Depends(get_async_session),
) -> list[ProductRead]:
    repository = ProductRepository(session)

    return await use_cases.read_products(
        repository=repository,
        filters=filters,
    )


@router.get("/{id}", response_model=ProductRead)
async def read_product(
    id: UUID,
    session: AsyncSession = Depends(get_async_session),
) -> ProductRead:
    try:
        repository = ProductRepository(session)
        return await use_cases.read_product(id, repository)
    except errors.NotFoundError as e:
        raise HTTPException(status_code=e.http_status_code, detail=str(e))
