from typing import Any, Coroutine
from sqlalchemy import delete
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.future import select

from db.models.user import User
from models.d_user import DUser
from db.helpers.user_mapper import to_domain_model
from db.helpers.hashing import Hashing
from core.config import PG_DSN
from repository.i_user_repository import IUserRepository, AddUserDTO, UpdateUserDTO


class UserRepository(IUserRepository):
    def __init__(self) -> None:
        super().__init__()
        self.engine = create_async_engine(PG_DSN, echo=True, future=True)
        self._model = User
        self.hashing = Hashing()

    async def add(self, dto: AddUserDTO, *args, **kwargs) -> Coroutine[Any, Any, None]:
        async with AsyncSession(self.engine) as session:
            hash_password = self.hashing.get_hashed_password(dto.password)
            user = User(login=dto.login, password=hash_password)
            session.add(user)
            await session.commit()
        
    async def get(self, *args, **kwargs) -> list[DUser]:
        async with AsyncSession(self.engine) as session:
            query = select(self._model)
            references = (await session.scalars(query)).all()
            return [to_domain_model(**references)]
        
    async def get_by_password_and_logon(self, login: str, password: str, *args, **kwargs) -> DUser | None:
        async with AsyncSession(self.engine) as session:
            query = select(self._model).where(self._model.login == login and self.hashing.verify_password(password, self._model.password))
            user = (await session.execute(query)).unique().scalars().all()
            if len(user) == 0:
                return None
            return to_domain_model(user[0])
        
    async def get_by_id(self, id: int, *args, **kwargs) -> DUser | None:
        async with AsyncSession(self.engine) as session:
            query = select(self._model).where(self._model.id == id)
            user = (await session.execute(query)).unique().scalar()
            if user is None:
                return None
            return to_domain_model(user)
        
    async def update(self, dto: UpdateUserDTO, *args, **kwargs) -> None:
        ...

    async def delete(self, id: int) -> None:
        async with AsyncSession(self.engine) as session:
            query = delete(self._model).where(self._model.id == id)
            await session.delete(query)
