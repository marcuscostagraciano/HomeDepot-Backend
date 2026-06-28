from fastapi import Depends, HTTPException

from core.domain import BaseError

from ..domain import ProductFilters
from ..schemas import ProductQueryParams


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
