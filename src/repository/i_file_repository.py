from datetime import datetime
from abc import abstractmethod

from models.d_file import DFile
from repository.i_repository import IRepository

class AddFileDTO:
    def __init__(
        self,
        name: str, 
        path: str, 
        size: str, 
        is_downloadable: bool, 
        user_id: int
        ) -> None:
        self.name = name
        self.path = path
        self.size = size
        self.is_downloadable = is_downloadable
        self.user_id = user_id

class UpdateFileDTO:
    def __init__(
        self,
        _id: int, 
        name: str, 
        path: str, 
        size: str, 
        is_downloadable: bool, 
        user_id: int
        ) -> None:
        self.id = _id
        self.name = name
        self.path = path
        self.size = size
        self.is_downloadable = is_downloadable
        self.user_id = user_id


class IFileRepository(IRepository[DFile, AddFileDTO, UpdateFileDTO]):
    @abstractmethod
    async def get_by_user_id(self, user_id: int) -> list[DFile]:
        ...