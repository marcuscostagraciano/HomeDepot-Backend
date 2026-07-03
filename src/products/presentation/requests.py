from pydantic import Field

from core.presentation.requests import BaseRequestPresentation


class ProductCreateRequestPresentation(BaseRequestPresentation):
    name: str
    observation: str | None = Field(
        default=None,
        description="Observation about the list",
    )
