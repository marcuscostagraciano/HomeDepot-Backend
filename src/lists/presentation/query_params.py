from fastapi import Depends, HTTPException

from core.domain.errors import BaseError
from core.presentation import BaseQueryParamsPresentation

from ..domain.filters import ListFilters


class ListQueryParams(BaseQueryParamsPresentation):
    name: str | None = None
    observation: str | None = None
    bought: bool | None = None


# Não faz sentido esse método > achei que o router ia fazer a tradução do HTTP para domínio
def get_list_filters(
    params: ListQueryParams = Depends(),
) -> ListFilters:
    try:
        return ListFilters(**params.model_dump())
    except BaseError as e:
        raise HTTPException(
            status_code=e.http_status_code,
            detail=e.message,
        )
