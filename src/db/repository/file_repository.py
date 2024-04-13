from typing import Any, Coroutine
from datetime import datetime

from sqlalchemy import delete
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy import update
from sqlalchemy.future import select

from core.config import PG_DSN
from db.models.file import File
from models.d_file import DFile
from db.helpers.file_mapper import to_domain_model
from repository.i_file_repository import IFileRepository, AddFileDTO, UpdateFileDTO


class FileRepository(IFileRepository):
    def __init__(self) -> None:
        super().__init__()
        self.engine = create_async_engine(PG_DSN, echo=True, future=True)
        self._model = File

    async def get_by_user_id(self, user_id: int) -> Coroutine[Any, Any, list[DFile]]:
        """
        Возвращает все репозитории пользователя
        """
        async with AsyncSession(self.engine) as session:
            query = select(self._model).where(self._model.user_id == user_id)
            files = (await session.scalars(query)).unique().all()
            return [to_domain_model(file) for file in files]
    
    def get(self, *args, **kwargs) -> Coroutine[Any, Any, list[DFile]]:
        return super().get(*args, **kwargs)
    
    async def add(self, dto: AddFileDTO, *args, **kwargs) -> Coroutine[Any, Any, None]:
        async with AsyncSession(self.engine) as session:
            file = File(
                name = dto.name,
                path = dto.path,
                size = dto.size,
                is_downloadable = dto.is_downloadable,
                created_ad = datetime.now(),
                user_id = dto.user_id
                )
            session.add(file)
            await session.commit()
    
    async def update(self, dto: UpdateFileDTO, *args, **kwargs) -> Coroutine[Any, Any, None]:
        async with AsyncSession(self.engine) as session:
            query = (
                update(self._model)
                .values(
                    name = dto.name,
                    path = dto.path,
                    size = dto.size,
                    is_downloadable = dto.is_downloadable,
                    created_ad = datetime.now(),
                    user_id = dto.user_id
                )
                .filter(self._model.id == dto.id)
            )
            await session.execute(query)
            await session.commit()
    
    async def delete(self, _id: int) -> Coroutine[Any, Any, None]:
        await delete(self._model).where(self._model.id == _id)
