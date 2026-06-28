from typing import Tuple, TypeVar

from sqlalchemy import Select

from core.models import BaseModel
from core.schemas import BaseSchema

CreateSchema = TypeVar("CreateSchema", bound=BaseSchema)
Model = TypeVar("Model", bound=BaseModel)
RecordIdT = TypeVar("RecordIdT", contravariant=True)
ReturnSchema = TypeVar("ReturnSchema", bound=BaseSchema)
type QuerySelect[Model] = Select[Tuple[Model]]
