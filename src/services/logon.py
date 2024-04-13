from datetime import datetime, timedelta
from typing import Union, Any
from jose import jwt

from core.config import ACCESS_TOKEN_EXPIRE_MINUTES, JWT_SECRET_KEY, ALGORITHM, REFRESH_TOKEN_EXPIRE_MINUTES, JWT_REFRESH_SECRET_KEY
from models.d_user import DUser
from schemas.token import TokenSchema
from repository.i_user_repository import IUserRepository, AddUserDTO


class UserLogon:
    async def registration(self, user_dto: AddUserDTO, repository: IUserRepository):
        user = await repository.get_by_password_and_logon(user_dto.login, user_dto.password)
        if user is not None: raise ValueError("User with this data already exist")
        await repository.add(user_dto)

    async def authentication(self, login: str, password: str, repository: IUserRepository) -> TokenSchema | None:
        """
        Find user by repository.
        Raise ValueError if login and password is empty string
        """
        if login != "" and password != "":
            user = await repository.get_by_password_and_logon(login, password)
            if user is None: raise ValueError("Login or password are/is incorrect")
            return {
                "access_token": self.create_access_token(user.id),
                "refresh_token": self.create_refresh_token(user.id),
            }
        else:
            raise ValueError("Login and password must be not empty string")

    
    async def autherization(self, token: str, repository: IUserRepository) -> DUser:
        payload = jwt.decode(
            token, JWT_SECRET_KEY, algorithms=[ALGORITHM]
        )
        if datetime.fromtimestamp(payload["exp"]) < datetime.now():
            raise ValueError("Token expired")
        user = await repository.get_by_id(int(payload["sub"]))
        if user is None:
            raise ValueError("Token is not connect with user")
        return user
        

    def create_access_token(self, subject: Union[str, Any], expires_delta: int = None) -> str:
        if expires_delta is not None:
            expires_delta = datetime.now() + expires_delta
        else:
            expires_delta = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode = {"exp": expires_delta, "sub": str(subject)}
        encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, ALGORITHM)
        return encoded_jwt

    def create_refresh_token(self, subject: Union[str, Any], expires_delta: int = None) -> str:
        if expires_delta is not None:
            expires_delta = datetime.now() + expires_delta
        else:
            expires_delta = datetime.now() + timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)
        to_encode = {"exp": expires_delta, "sub": str(subject)}
        encoded_jwt = jwt.encode(to_encode, JWT_REFRESH_SECRET_KEY, ALGORITHM)
        return encoded_jwt