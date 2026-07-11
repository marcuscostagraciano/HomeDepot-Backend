from uuid import UUID

from core.presentation import BaseResponsePresentation


class ListShareReadResponsePresentation(BaseResponsePresentation):
    user_id: UUID
    list_id: UUID
