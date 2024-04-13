import logging

from pathlib import Path

from core.config import STATIC_DIR
from repository.i_user_repository import IUserRepository
from services.logon import UserLogon

async def file_upload(
    token: str,
    user_repository: IUserRepository,
    file: bytes,
    dir_path: str,
    file_name: str
    ) -> dict[str, str]:
    """
    Получение всех ссылок пользователя с авторизацией
    """
    logon = UserLogon()
    user = await logon.autherization(token, user_repository)
    path = Path()
    path = path.joinpath(STATIC_DIR, str(user.id), dir_path)
    if not path.exists():
        path.mkdir()
    path = path.joinpath(file_name)
    with open(str(path), 'wb') as f:
        f.write(file)
    return {"message": f"Successfully uploaded {str(path)}"}
         