import logging
from pathlib import Path
import aiofiles

from core.config import STATIC_DIR, PROJECT_HOST, PROJECT_PORT
from models.d_user import DUser
from models.d_file import DFile
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
         

async def get_files(
    token: str,
    user_repository: IUserRepository,
    file_repository: IFileRepository,
    ) -> list[DFile]:
    """
    Upload file with user autherization
    """
    logon = UserLogon()
    user = await logon.autherization(token, user_repository)
    results = await file_repository.get_by_user_id(user_id=user.id)
    return results


async def get_file_path(
    token: str,
    user_repository: IUserRepository,
    file_repository: IFileRepository,
    path: str,
    filename: str
    ):
    """
    Get file path with user autherization
    """
    files = await get_files(token, user_repository, file_repository)
    result = None
    for file in files:
        if file.name == filename and f"{STATIC_DIR}/{file.user_id}/{file.path}" == path:
            result = file
            break
    if result is None:
        raise ValueError(f"You cann't download this file {path}/{filename}")
    path = f"{STATIC_DIR}/{result.user_id}/{result.path}"
    if PROJECT_HOST == '0.0.0.0':
        path = f"http://localhost:81/{path}"
    else: 
        path = f"http://{PROJECT_HOST}:81/{path}"
    return path