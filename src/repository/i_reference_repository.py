from abc import abstractmethod

from .i_repository import IRepository
from models.d_reference import DReference, VisibilityType

class AddReferenceDTO:
    def __init__(self, short_id: str, short_url: str, original_url: str, visibility: VisibilityType, user_id: int) -> None:
        self.short_id: str = short_id
        self.short_url: str = short_url
        self.original_url: str = original_url
        self.visibility = visibility
        self.user_id: int = user_id

class UpdateReferenceDTO:
    def __init__(self, short_id: str, short_url: str, original_url: str, visibility: VisibilityType, user_id: int) -> None:
        self.short_id: str = short_id
        self.short_url: str = short_url
        self.original_url: str = original_url
        self.visibility = visibility
        self.user_id: int = user_id

class IReferenceRepository(IRepository[DReference, AddReferenceDTO, UpdateReferenceDTO]):

    @abstractmethod
    def add_batch_references(self, dtos: list[AddReferenceDTO]) -> None:
        ...

    @abstractmethod
    def get_by_user_id(self, user_id: int) -> list[DReference]:
        ...

    @abstractmethod
    def get_private_by_user_id(self, user_id: int) -> list[DReference]:
        ...

    @abstractmethod
    def get_by_short_id(self, short_id: str) -> DReference:
        ...

    @abstractmethod
    def get_short_urls_by_original(self, original_url: str, user_id: int = None) -> list[str]:
        ...