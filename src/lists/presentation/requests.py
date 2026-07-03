from pydantic import Field

from core.presentation import BaseRequestPresentation


class ListCreateRequestPresentation(BaseRequestPresentation):
    name: str
    observation: str | None = Field(
        default=None,
        description="Observation about the list",
    )
