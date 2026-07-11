from uuid import UUID

from core.domain.errors import NotFoundError
from lists.domain.ports import ListRepositoryPort
from products.domain.ports import ProductRepositoryPort
from shared.list_shares.domain.ports import ListShareRepositoryPort
from shared.list_shares.domain.use_cases import validate_user_access_to_list

from ...domain.types import AssociationIdVO
from ..domain.ports import ListProductRepositoryPort
from ..domain.schemas import ListProductCreate, ListProductRead, ListProductUpdate


async def add_product_to_list(
    repository: ListProductRepositoryPort,
    list_repository: ListRepositoryPort,
    product_repository: ProductRepositoryPort,
    share_repository: ListShareRepositoryPort,
    payload: ListProductCreate,
    user_id: UUID,
) -> ListProductRead:
    await validate_user_access_to_list(
        share_repository,
        list_repository,
        payload.list_id,
        user_id,
    )

    product_obj = await product_repository.read(payload.product_id)
    if not product_obj:
        raise NotFoundError("Product", str(payload.product_id))

    return await repository.create(payload)


async def read_list_products(
    repository: ListProductRepositoryPort,
    list_repository: ListRepositoryPort,
    share_repository: ListShareRepositoryPort,
    list_id: UUID,
    user_id: UUID,
) -> list[ListProductRead]:
    await validate_user_access_to_list(
        share_repository,
        list_repository,
        list_id,
        user_id,
    )

    return await repository.read_all_by_list(list_id)


async def update_list_product(
    repository: ListProductRepositoryPort,
    list_repository: ListRepositoryPort,
    share_repository: ListShareRepositoryPort,
    id: AssociationIdVO,
    payload: ListProductUpdate,
    user_id: UUID,
) -> ListProductRead:
    await validate_user_access_to_list(
        share_repository,
        list_repository,
        id.first_id,
        user_id,
    )

    updated = await repository.update(id, payload)

    if not updated:
        raise NotFoundError("ListProduct", str(id))

    return updated


async def delete_list_product(
    repository: ListProductRepositoryPort,
    list_repository: ListRepositoryPort,
    share_repository: ListShareRepositoryPort,
    id: AssociationIdVO,
    user_id: UUID,
) -> ListProductRead:
    await validate_user_access_to_list(
        share_repository,
        list_repository,
        id.first_id,
        user_id,
    )

    deleted = await repository.delete(id)

    if not deleted:
        raise NotFoundError("ListProduct", str(id))

    return deleted
