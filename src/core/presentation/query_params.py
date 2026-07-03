from pydantic import Field

from ..domain.enums import SortFieldEnum, SortOrderEnum
from .base_presentation import BasePresentation


class BaseQueryParamsPresentation(BasePresentation):
    """Schema used as a base for all query parameters."""

    page: int = Field(
        default=1,
        description="Page number for paginated results. Starts at 1.",
    )
    limit: int = Field(
        default=20,
        description="Maximum number of items to return per page.",
    )
    sort: SortFieldEnum = Field(
        default=SortFieldEnum.ID,
        description="Field used to sort the returned results.",
    )
    order: SortOrderEnum = Field(
        default=SortOrderEnum.ASC,
        description="Sort order for the returned results (ascending or descending).",
    )
