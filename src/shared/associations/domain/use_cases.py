from uuid import UUID

from core.domain.errors import NotFoundError
from lists.domain.ports import ListRepositoryPort
from products.domain.ports import ProductRepositoryPort

from ..domain.ports import ListProductRepositoryPort
from ..domain.schemas import ListProductCreate, ListProductRead, ListProductUpdate


async def add_product_to_list(
    repository: ListProductRepositoryPort,
    list_repository: ListRepositoryPort,
    product_repository: ProductRepositoryPort,
    payload: ListProductCreate,
) -> ListProductRead:
    list_obj = await list_repository.read(payload.list_id)
    if not list_obj:
        raise NotFoundError("List", str(payload.list_id))

    product_obj = await product_repository.read(payload.product_id)
    if not product_obj:
        raise NotFoundError("Product", str(payload.product_id))

    return await repository.create(payload)


async def read_list_products(
    repository: ListProductRepositoryPort,
    list_id: UUID,
) -> list[ListProductRead]:
    return await repository.read_all_by_list(list_id)


async def update_list_product(
    repository: ListProductRepositoryPort,
    list_id: UUID,
    product_id: UUID,
    payload: ListProductUpdate,
) -> ListProductRead:

    updated = await repository.update(
        (list_id, product_id),
        payload,
    )

    if not updated:
        raise NotFoundError("ListProduct", f"{list_id}/{product_id}")

    return updated


async def delete_list_product(
    repository: ListProductRepositoryPort,
    list_id: UUID,
    product_id: UUID,
) -> ListProductRead:
    deleted = await repository.delete((list_id, product_id))

    if not deleted:
        raise NotFoundError("ListProduct", f"{list_id}/{product_id}")

    return deleted
