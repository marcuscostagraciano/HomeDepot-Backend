from uuid import UUID

from fastapi import APIRouter, Depends

from core.presentation.dependencies import RequestContext, get_request_context

from ..domain.filters import ProductFilters
from ..domain.schemas import ProductCreate
from ..domain.use_cases import create_product as create_product_case
from ..domain.use_cases import read_product as read_product_case
from ..domain.use_cases import read_products as read_products_case
from ..presentation.query_params import get_products_filters
from ..presentation.requests import ProductCreateRequestPresentation as CreateRequest
from ..presentation.responses import ProductReadResponsePresentation as Response
from ..repositories.product_repository import ProductRepository

router = APIRouter(prefix="/products", tags=["products"])


@router.post("/", response_model=Response)
async def create_product(
    payload: CreateRequest,
    context: RequestContext = Depends(get_request_context),
) -> Response:
    created = await create_product_case(
        ProductRepository(context.session),
        ProductCreate.from_dict(payload.to_dict()),
        context.user.id,
    )

    return Response.from_dict(created.to_dict())


@router.get("", response_model=list[Response])
async def read_products(
    filters: ProductFilters = Depends(get_products_filters),
    context: RequestContext = Depends(get_request_context),
) -> list[Response]:

    products = await read_products_case(
        ProductRepository(context.session),
        filters,
    )

    return [Response.from_dict(obj.to_dict()) for obj in products]


@router.get("/{id}", response_model=Response)
async def read_product(
    id: UUID,
    context: RequestContext = Depends(get_request_context),
) -> Response:
    product = await read_product_case(
        ProductRepository(context.session),
        id,
    )

    return Response.from_dict(product.to_dict())
