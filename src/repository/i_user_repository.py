from .i_repository import IRepository
from models.d_user import DUser
from models.d_reference import DReference
from abc import abstractmethod

class AddUserDTO:
    def __init__(self, login: str, password: str) -> None:
        self.login = login
        self.password = password

class UpdateUserDTO:
    def __init__(self, _id: int, login: str, password: str) -> None:
        self.id = _id
        self.login = login
        self.password = password

class IUserRepository(IRepository[DUser, AddUserDTO, UpdateUserDTO]):

    @abstractmethod
    async def get_by_id(self, id: int, *args, **kwargs) -> DUser | None:
        ...

    @abstractmethod
    async def get_by_password_and_logon(self, login: str, password: str, *args, **kwargs) -> DUser | None:
        ...
    