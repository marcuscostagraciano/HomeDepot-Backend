from uuid import UUID

from fastapi import APIRouter, Depends

from core.presentation.dependencies import RequestContext, get_request_context

from ..domain.filters import ListFilters
from ..domain.schemas import ListCreate
from ..domain.use_cases import create_list as create_list_case
from ..domain.use_cases import delete_list as delete_list_case
from ..domain.use_cases import read_list as read_list_case
from ..domain.use_cases import read_lists as read_lists_case
from ..presentation.query_params import get_list_filters
from ..presentation.requests import ListCreateRequestPresentation as CreateRequest
from ..presentation.responses import ListReadResponsePresentation as Response
from ..repositories.list_repository import ListRepository

router = APIRouter(prefix="/lists", tags=["lists"])


@router.post("/", response_model=Response)
async def create_list(
    list_create: CreateRequest,
    context: RequestContext = Depends(get_request_context),
) -> Response:
    created = await create_list_case(
        ListRepository(context.session),
        ListCreate.from_dict(list_create.to_dict()),
        context.user.id,
    )

    return Response.from_dict(created.to_dict())


@router.get("", response_model=list[Response])
async def read_lists(
    filters: ListFilters = Depends(get_list_filters),
    context: RequestContext = Depends(get_request_context),
) -> list[Response]:
    repository = ListRepository(context.session)
    lists = await read_lists_case(repository, filters)

    return [Response.from_dict(obj.to_dict()) for obj in lists]


@router.get("/{list_id}", response_model=Response)
async def read_list(
    list_id: UUID,
    context: RequestContext = Depends(get_request_context),
) -> Response:
    repository = ListRepository(context.session)
    list = await read_list_case(repository, list_id)

    return Response.from_dict(list.to_dict())


@router.delete("/{list_id}", response_model=Response)
async def delete_list(
    list_id: UUID,
    context: RequestContext = Depends(get_request_context),
):
    list = await delete_list_case(
        ListRepository(context.session),
        list_id,
        context.user.id,
    )

    return Response.from_dict(list.to_dict())
