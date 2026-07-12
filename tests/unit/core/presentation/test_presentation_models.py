from datetime import datetime
from typing import Any
from uuid import UUID

from core.presentation.base_presentation import BasePresentation
from core.presentation.query_params import BaseQueryParamsPresentation
from core.presentation.requests import BaseRequestPresentation
from core.presentation.responses import BaseResponsePresentation


class DummyPresentation(BasePresentation):
    value: int


class DummyRequest(BaseRequestPresentation):
    name: str


class DummyResponse(BaseResponsePresentation):
    name: str


class DummyQueryParams(BaseQueryParamsPresentation):
    pass


def test_base_presentation_to_dict_and_from_dict() -> None:
    original = DummyPresentation(value=42)

    assert original.to_dict() == {"value": 42}
    copy = DummyPresentation.from_dict(original.to_dict())
    assert copy.value == 42


def test_request_and_response_presentations_serialization() -> None:
    created = DummyRequest(name="a")
    assert created.to_dict() == {"name": "a"}

    response = DummyResponse(
        id=UUID("11111111-1111-1111-1111-111111111111"),
        created_date=datetime(2020, 1, 1),
        updated_date=None,
        name="a",
    )
    assert response.to_dict()["name"] == "a"


def test_base_query_params_defaults() -> None:
    query = DummyQueryParams()

    assert query.page == 1
    assert query.limit == 20
    assert query.sort == query.sort
    assert query.order == query.order
    assert query.to_dict()["page"] == 1
