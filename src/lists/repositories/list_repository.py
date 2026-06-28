from sqlalchemy.ext.asyncio import AsyncSession

from db.adapters.sqlalchemy_repository import SQLAlchemyRepository

from ..domain.ports import ListRepositoryPort
from ..models import List
from ..schemas.list import ListCreate, ListRead


class ListRepository(
    SQLAlchemyRepository[ListCreate, List, ListRead],
    ListRepositoryPort,
):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session=session, model=List, schema=ListRead)
