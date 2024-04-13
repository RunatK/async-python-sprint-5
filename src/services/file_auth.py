import logging
from pathlib import Path
import aiofiles

from core.config import STATIC_DIR
from models.d_user import DUser
from repository.i_user_repository import IUserRepository
from repository.i_file_repository import IFileRepository, AddFileDTO
from services.logon import UserLogon

async def file_upload(
    token: str,
    user_repository: IUserRepository,
    file_repository: IFileRepository,
    file: bytes,
    dir_path: str,
    file_name: str,
    size: int
    ) -> dict[str, str]:
    """
    Upload file with user autherization
    """
    logon = UserLogon()
    user = await logon.autherization(token, user_repository)
    path = await create_file(user, file, dir_path, file_name)
    dto = AddFileDTO(
        name=file_name,
        path=dir_path,
        size=size,
        is_downloadable=True,
        user_id=user.id
    )
    await file_repository.add(dto)
    return {"message": f"Successfully uploaded {str(path)}"}


async def create_file(user: DUser, file: bytes, dir_path: str, file_name: str) -> str:
    path = Path()
    path = path.joinpath(STATIC_DIR, str(user.id), dir_path)
    if not path.exists():
        path.mkdir()
    path = path.joinpath(file_name)
    async with aiofiles.open(str(path), 'wb') as f:
        await f.write(file)
    return path
         