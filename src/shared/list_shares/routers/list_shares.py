from uuid import UUID

from fastapi import APIRouter, Depends

from core.presentation.dependencies import RequestContext, get_request_context
from lists.repositories.list_repository import ListRepository
from users.repositories.user_repository import UserRepository

from ...domain.types import AssociationIdVO
from ..domain.schemas import UserListCreate
from ..domain.use_cases import read_shared_lists, share_list
from ..domain.use_cases import remove_share as remove_share_case
from ..presentation.requests import ListShareCreateRequestPresentation as CreateRequest
from ..presentation.responses import ListShareReadResponsePresentation as Response
from ..repositories.list_share_repository import ListShareRepository

router = APIRouter(prefix="/list-shares", tags=["list-shares"])


@router.post("/", response_model=Response)
async def share_list_with_user(
    payload: CreateRequest,
    context: RequestContext = Depends(get_request_context),
) -> Response:
    repository = ListShareRepository(context.session)
    list_repository = ListRepository(context.session)
    user_repository = UserRepository(context.session)

    shared = await share_list(
        repository,
        list_repository,
        user_repository,
        UserListCreate.from_dict(payload.to_dict()),
        context.user.id,
    )

    return Response.from_dict(shared.to_dict())


@router.get("/", response_model=list[Response])
async def read_my_shared_lists(
    context: RequestContext = Depends(get_request_context),
) -> list[Response]:
    repository = ListShareRepository(context.session)
    shared = await read_shared_lists(repository, context.user.id)

    return [Response.from_dict(item.to_dict()) for item in shared]


@router.delete("/{list_id}/users/{user_id}", response_model=Response)
async def remove_share_from_list(
    list_id: UUID,
    user_id: UUID,
    context: RequestContext = Depends(get_request_context),
) -> Response:
    repository = ListShareRepository(context.session)
    list_repository = ListRepository(context.session)
    association_id = AssociationIdVO(user_id, list_id)

    deleted = await remove_share_case(
        repository,
        list_repository,
        context.user.id,
        association_id,
    )

    return Response.from_dict(deleted.to_dict())
