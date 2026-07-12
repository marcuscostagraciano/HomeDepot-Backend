import uuid

from sqlalchemy import String
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import Mapped, mapped_column

from core.models.auditable import AuditableModel
from core.models.base import BaseModel


class DummyBase(BaseModel):
    name: Mapped[str] = mapped_column(String(10), nullable=False)


class DummyAuditable(AuditableModel):
    name: Mapped[str] = mapped_column(String(10), nullable=False)


def test_base_model_to_dict_and_tablename() -> None:
    instance = DummyBase(name="test")

    result = instance.to_dict()

    assert result["name"] == "test"
    assert instance.__tablename__ == "dummybase"
    assert "id" in result


def test_auditable_model_inherits_uuid_fields() -> None:
    created_by_id = uuid.uuid4()
    instance = DummyAuditable(name="test", created_by_id=created_by_id)

    result = instance.to_dict()

    assert result["name"] == "test"
    assert result["created_by_id"] == created_by_id
    assert instance.__tablename__ == "dummyauditable"
