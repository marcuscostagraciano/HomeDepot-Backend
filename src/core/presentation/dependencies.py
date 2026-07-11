from dataclasses import dataclass

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from db.db import get_async_session
from users.domain.schemas import UserRead
from users.presentation.dependencies import get_current_user


@dataclass
class RequestContext:
    session: AsyncSession
    user: UserRead


async def get_request_context(
    session: AsyncSession = Depends(get_async_session),
    user: UserRead = Depends(get_current_user),
) -> RequestContext:
    return RequestContext(session, user)
