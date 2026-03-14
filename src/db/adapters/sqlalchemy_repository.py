from typing import Any, Type
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from core.models import BaseModel
from core.schemas import BaseSchema


class SQLAlchemyRepository:
    def __init__(self, session: AsyncSession, model: Type[BaseModel]) -> None:
        self.session = session
        self.model = model

    async def create(self, payload: BaseSchema) -> Any:
        db_obj = self.model(**payload.model_dump())

        self.session.add(db_obj)
        await self.session.commit()
        await self.session.refresh(db_obj)

        return db_obj

    async def read(self, id: UUID) -> Any | None:
        return await self.session.get(self.model, id)
