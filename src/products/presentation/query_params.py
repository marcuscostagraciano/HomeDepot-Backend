from fastapi import Depends, HTTPException

from core.domain.errors import BaseError
from core.presentation.query_params import BaseQueryParamsPresentation

from ..domain.filters import ProductFilters


class ProductQueryParams(BaseQueryParamsPresentation):
    name: str | None = None
    brand: str | None = None
    min_price: float | None = None
    max_price: float | None = None


def get_products_filters(
    params: ProductQueryParams = Depends(),
) -> ProductFilters:
    try:
        return ProductFilters(**params.model_dump())
    except BaseError as e:
        raise HTTPException(
            status_code=e.http_status_code,
            detail=e.message,
        )
