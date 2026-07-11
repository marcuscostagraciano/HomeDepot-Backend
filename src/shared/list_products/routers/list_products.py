from uuid import UUID

from fastapi import APIRouter, Depends

from core.presentation.dependencies import RequestContext, get_request_context
from lists.repositories.list_repository import ListRepository
from products.repositories.product_repository import ProductRepository
from shared.list_shares.repositories.list_share_repository import ListShareRepository

from ...domain.types import AssociationIdVO
from ..domain.schemas import ListProductCreate, ListProductUpdate
from ..domain.use_cases import add_product_to_list as add_product_to_list_case
from ..domain.use_cases import delete_list_product as delete_list_product_case
from ..domain.use_cases import read_list_products as read_list_products_case
from ..domain.use_cases import update_list_product as update_list_product_case
from ..presentation.requests import (
    ListProductCreateRequestPresentation as CreateRequest,
)
from ..presentation.requests import (
    ListProductUpdateRequestPresentation as UpdateRequest,
)
from ..presentation.responses import ListProductReadResponsePresentation as Response
from ..repositories.list_product_repository import ListProductRepository

router = APIRouter(prefix="/lists/{list_id}/products", tags=["list-products"])


@router.post("/", response_model=Response)
async def add_product_to_list(
    list_id: UUID,
    payload: CreateRequest,
    context: RequestContext = Depends(get_request_context),
) -> Response:
    repository = ListProductRepository(context.session)
    list_repository = ListRepository(context.session)
    product_repository = ProductRepository(context.session)
    share_repository = ListShareRepository(context.session)

    payload_data = payload.to_dict()
    payload_data["list_id"] = list_id

    created = await add_product_to_list_case(
        repository,
        list_repository,
        product_repository,
        share_repository,
        ListProductCreate.from_dict(payload_data),
        context.user.id,
    )

    return Response.from_dict(created.to_dict())


@router.get("/", response_model=list[Response])
async def read_list_products(
    list_id: UUID,
    context: RequestContext = Depends(get_request_context),
) -> list[Response]:
    repository = ListProductRepository(context.session)
    list_repository = ListRepository(context.session)
    share_repository = ListShareRepository(context.session)

    items = await read_list_products_case(
        repository,
        list_repository,
        share_repository,
        list_id,
        context.user.id,
    )

    return [Response.from_dict(item.to_dict()) for item in items]


@router.patch("/{product_id}", response_model=Response)
async def update_list_product(
    list_id: UUID,
    product_id: UUID,
    payload: UpdateRequest,
    context: RequestContext = Depends(get_request_context),
) -> Response:
    repository = ListProductRepository(context.session)
    list_repository = ListRepository(context.session)
    share_repository = ListShareRepository(context.session)
    id_vo = AssociationIdVO(list_id, product_id)

    updated = await update_list_product_case(
        repository,
        list_repository,
        share_repository,
        id_vo,
        ListProductUpdate.from_dict(payload.to_dict()),
        context.user.id,
    )

    return Response.from_dict(updated.to_dict())


@router.delete("/{product_id}", response_model=Response)
async def delete_list_product(
    list_id: UUID,
    product_id: UUID,
    context: RequestContext = Depends(get_request_context),
) -> Response:
    repository = ListProductRepository(context.session)
    list_repository = ListRepository(context.session)
    share_repository = ListShareRepository(context.session)
    id_vo = AssociationIdVO(list_id, product_id)

    deleted = await delete_list_product_case(
        repository,
        list_repository,
        share_repository,
        id_vo,
        context.user.id,
    )

    return Response.from_dict(deleted.to_dict())
