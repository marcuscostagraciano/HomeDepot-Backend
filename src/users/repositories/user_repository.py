from sqlalchemy.ext.asyncio import AsyncSession

from db.adapters.sqlalchemy_repository import SQLAlchemyRepository
from users.domain.ports import UserRepositoryPort
from users.models.user import User


class UserRepository(
    SQLAlchemyRepository,
    UserRepositoryPort,
):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session=session, model=User)
