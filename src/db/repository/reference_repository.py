from sqlalchemy import delete
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy import update
from sqlalchemy.future import select

from db.models.reference import Reference
from models.d_reference import DReference, VisibilityType
from db.helpers.reference_mapper import to_domain_model
from core.config import PG_DSN
from repository.i_reference_repository import AddReferenceDTO, IReferenceRepository, UpdateReferenceDTO

class ReferenceRepository(IReferenceRepository):
    def __init__(self) -> None:
        super().__init__()
        self.engine = create_async_engine(PG_DSN, echo=True, future=True)
        self._model = Reference
        self.MAX_SIZE_SHORT_ID = 255

    async def add(self, dto: AddReferenceDTO):
        async with AsyncSession(self.engine) as session:
            if len(dto.short_id) > self.MAX_SIZE_SHORT_ID:
                raise ValueError(f"short_id must have {self.MAX_SIZE_SHORT_ID} symbol or smaller")
            reference = Reference(
                short_id=dto.short_id,
                short_url=dto.short_url, 
                original_url=dto.original_url, 
                visibility=dto.visibility,
                user_id=dto.user_id
                )
            session.add(reference)
            await session.commit()

    async def add_batch_references(self, dtos: list[AddReferenceDTO]) -> None:
        async with AsyncSession(self.engine) as session:
            for dto in dtos:
                if len(dto.short_id) > self.MAX_SIZE_SHORT_ID:
                    raise ValueError(f"short_id must have {self.MAX_SIZE_SHORT_ID} symbol or smaller")
                reference = Reference(
                    short_id=dto.short_id,
                    short_url=dto.short_url, 
                    original_url=dto.original_url, 
                    visibility=dto.visibility,
                    user_id=dto.user_id
                    )
                session.add(reference)
            await session.commit()

    async def get_by_user_id(self, user_id: int) -> list[DReference]:
        """
        Возвращает все репозитории пользователя
        """
        async with AsyncSession(self.engine) as session:
            query = select(self._model).where(self._model.user_id == user_id)
            references = (await session.scalars(query)).unique().all()
            return [to_domain_model(reference) for reference in references]
        
    async def get_private_by_user_id(self, user_id: int) -> list[DReference]:
        """
        Возвращает все приватные репозитории пользователя
        """
        async with AsyncSession(self.engine) as session:
            query = select(self._model).where(self._model.user_id == user_id and self._model.user_id == VisibilityType.private.name)
            references = (await session.scalars(query)).unique().all()
            return [to_domain_model(reference) for reference in references]
        
    async def get_by_short_id(self, short_id: str) -> DReference:
        """
        Возвращает оригинальный URL по укороченному id
        """
        async with AsyncSession(self.engine) as session:
            query = select(self._model).where(self._model.short_id == short_id)
            reference = (await session.scalar(query))
            return to_domain_model(reference)
        
    async def get_short_urls_by_original(self, original_url: str, user_id: int = None) -> list[str]:
        """
        Возвращает все укороченные URL для оригинального
        """
        async with AsyncSession(self.engine) as session:
            query = select(self._model.short_url).where(self._model.original_url == original_url)
            if user_id is not None:
                query = query.where(self._model.user_id == user_id or self._model.visibility == VisibilityType.public.name)
            else:
                query = query.where(self._model.visibility == VisibilityType.public.name)
            references = (await session.scalars(query)).unique().all()
            return str(references)
        
    async def get(self) -> list[DReference]:
        """
        Возвращает все публичные репозитории
        """
        async with AsyncSession(self.engine) as session:
            query = select(self._model).where(self._model.visibility == VisibilityType.public.name)
            references = (await session.execute(query)).unique().scalars().all()
            return [to_domain_model(reference) for reference in references]

    async def update(self, dto: UpdateReferenceDTO, *args, **kwargs) -> None:
        async with AsyncSession(self.engine) as session:
            query = (
                update(self._model)
                .values(
                    short_url = dto.short_url,
                    original_url = dto.original_url,
                    visibility = dto.visibility.name
                )
                .filter(self._model.short_id == dto.short_id,)
            )
            await session.execute(query)
            await session.commit()
        
    async def delete(self, id: int) -> None:
        await delete(self._model).where(self._model.id == id)
        