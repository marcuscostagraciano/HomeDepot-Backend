from datetime import datetime
from typing import Dict
from uuid import UUID

from sqlalchemy.orm import InstrumentedAttribute

from core.domain import SortField

type SortFieldMapping = Dict[SortField, InstrumentedAttribute[UUID | datetime | None]]
