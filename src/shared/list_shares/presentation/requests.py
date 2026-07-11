from uuid import UUID

from pydantic import Field

from core.presentation import BaseRequestPresentation


class ListShareCreateRequestPresentation(BaseRequestPresentation):
    user_id: UUID
    list_id: UUID
