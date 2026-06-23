from sqlalchemy.ext.asyncio import AsyncSession

from db.adapters.sqlalchemy_repository import SQLAlchemyRepository
from lists.domain.ports import ListRepositoryPort
from lists.models import List


class ListRepository(SQLAlchemyRepository, ListRepositoryPort):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session=session, model=List)
