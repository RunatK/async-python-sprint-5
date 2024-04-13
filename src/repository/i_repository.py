from abc import ABC, abstractmethod
from typing import TypeVar, Generic

E = TypeVar('E')
AddDto = TypeVar("AddDto")
UpdateDto = TypeVar("UpdateDto")

class IRepository(ABC, Generic[E, AddDto, UpdateDto]):
    """
    Base repository interface
    """

    @abstractmethod
    async def get(self, *args, **kwargs) -> list[E]:
        ...

    @abstractmethod
    async def add(self, dto: AddDto, *args, **kwargs) -> None:
        ...

    @abstractmethod
    async def update(self, dto: UpdateDto, *args, **kwargs) -> None:
        ...
    
    @abstractmethod
    async def delete(self, *args, **kwargs) -> None:
        ...