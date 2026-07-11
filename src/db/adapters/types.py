from datetime import datetime
from typing import Dict, TypeVar
from uuid import UUID

from sqlalchemy.orm import InstrumentedAttribute

from core.domain.enums import SortFieldEnum
from core.models.base import BaseModel

ORMModelT = TypeVar("ORMModelT", bound=BaseModel)
type SortFieldMapping = Dict[
    SortFieldEnum, InstrumentedAttribute[UUID | datetime | None]
]
