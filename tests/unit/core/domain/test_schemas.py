from dataclasses import dataclass
from typing import Any

from core.domain.schemas import DomainCreateSchema, DomainReadSchema, DomainSchema


@dataclass(frozen=True)
class DummySchema(DomainSchema):
    value: int


@dataclass(frozen=True)
class DummyReadSchema(DummySchema, DomainReadSchema):
    id: str
    created_date: str
    updated_date: str | None


def test_domain_schema_to_dict_and_from_dict() -> None:
    payload = {"value": 5}

    schema = DummySchema.from_dict(payload)
    assert schema.to_dict() == payload

    copied = schema.copy(update={"value": 10})
    assert copied.value == 10
    assert schema.value == 5


def test_domain_read_schema_includes_base_fields() -> None:
    values = {
        "value": 1,
        "id": "uuid",
        "created_date": "now",
        "updated_date": None,
    }

    read_schema = DummyReadSchema.from_dict(values)
    assert read_schema.id == "uuid"
    assert read_schema.created_date == "now"
    assert read_schema.updated_date is None
    assert read_schema.copy().to_dict() == values
