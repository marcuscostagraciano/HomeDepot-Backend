from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

import core.errors as errors
from db.db import get_async_session
from products.domain import use_cases
from products.repositories.product_repository import ProductRepository
from products.schemas import ProductCreate, ProductRead

router = APIRouter(
    prefix="/products", tags=["products"], dependencies=[Depends(get_async_session)]
)


@router.post("/", response_model=ProductRead)
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


@router.get("/", response_model=List[ProductRead])
async def read_products(
    session: AsyncSession = Depends(get_async_session),
) -> List[ProductRead]:
    try:
        repository = ProductRepository(session)
        products = await use_cases.read_products(repository)
    except errors.NotFoundError as e:
        raise HTTPException(status_code=e.http_status_code, detail=str(e))

    return products


@router.get("/{id}", response_model=List[ProductRead])
async def read_product(
    id: UUID,
    session: AsyncSession = Depends(get_async_session),
) -> ProductRead | None:
    try:
        repository = ProductRepository(session)
        product = await use_cases.read_product(id, repository)
    except errors.NotFoundError as e:
        raise HTTPException(status_code=e.http_status_code, detail=str(e))

    return product


# @router.get("/", response_model=List[ProductRead])
# async def read_products(
#     offset: int = 0,
#     limit: int = 100,
#     search: str | None = None,
#     brand: str | None = None,
#     min_price: float | None = None,
#     max_price: float | None = None,
#     sort_by: str = "name",
#     sort_order: str = "asc",
#     session: AsyncSession = Depends(get_async_session),
# ) -> List[ProductRead]:
#     query = select(Product)

#     # Apply filters
#     filters = []
#     if search:
#         filters.append(
#             (Product.name.ilike(f"%{search}%"))
#             | (Product.description.ilike(f"%{search}%"))
#         )
#     if brand:
#         filters.append(Product.brand == brand)
#     if min_price is not None:
#         filters.append(Product.price >= min_price)
#     if max_price is not None:
#         filters.append(Product.price <= max_price)

#     if filters:
#         query = query.where(and_(*filters))

#     # Apply sorting
#     sort_column = getattr(Product, sort_by, Product.name)
#     if sort_order.lower() == "desc":
#         query = query.order_by(sort_column.desc())
#     else:
#         query = query.order_by(sort_column.asc())

#     # Apply pagination
#     query = query.offset(offset).limit(limit)

#     result = await session.execute(query)
#     products = result.scalars().all()
#     return [ProductRead.model_validate(product) for product in products]


# @router.patch("/{product_id}", response_model=ProductRead)
# async def update_product(
#     product_id: UUID,
#     payload: ProductUpdate,
#     session: AsyncSession = Depends(get_async_session),
# ) -> ProductRead:
#     result = await session.execute(select(Product).where(Product.id == product_id))
#     product = result.scalar_one_or_none()

#     if product is None:
#         raise HTTPException(
#             status_code=HTTPStatus.NOT_FOUND, detail=f"{Product.__name__} not found"
#         )

#     update_data = payload.model_dump(exclude_unset=True)
#     for key, value in update_data.items():
#         setattr(product, key, value)

#     await session.commit()
#     await session.refresh(product)

#     return ProductRead.model_validate(product)


# @router.delete("/{product_id}")
# async def delete_product(
#     product_id: UUID,
#     session: AsyncSession = Depends(get_async_session),
# ) -> dict[str, bool]:
#     result = await session.execute(select(Product).where(Product.id == product_id))
#     product = result.scalar_one_or_none()

#     if product is None:
#         raise HTTPException(
#             status_code=HTTPStatus.NOT_FOUND, detail=f"{Product.__name__} not found"
#         )

#     await session.delete(product)
#     await session.commit()

#     return {"success": True}
#     return {"success": True}
#     return {"success": True}
#     return {"success": True}
