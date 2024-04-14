from typing import Optional

from fastapi import APIRouter, Depends, UploadFile, File
from fastapi.responses import FileResponse
from fastapi.security import OAuth2PasswordBearer

from api.dependencies import get_user_repository, get_file_repository
from repository.i_user_repository import IUserRepository
from repository.i_file_repository import IFileRepository
from services.file_auth import file_upload, get_files, get_file_path
from core.config import STATIC_DIR


router = APIRouter()

reuseable_oauth = OAuth2PasswordBearer(
    tokenUrl="v1/login",
    scheme_name="UserAuth"
)

@router.post("/upload_file/", summary="Upload file to dir")
async def create_upload_file(
    file: UploadFile,
    dir_path: Optional[str] = "",
    token: str = Depends(reuseable_oauth),
    user_repository: IUserRepository = Depends(get_user_repository),
    file_repository: IFileRepository = Depends(get_file_repository)
    ):
    result = {}
    try:
        contents = file.file.read()
        result = await file_upload(token, user_repository, file_repository, contents, dir_path, file.filename, file.size)
    except Exception as e:
        result = {"message": f"There was an error uploading the file {e}"}
        raise e
    finally:
        file.file.close()
    return result

@router.get("/get_files", summary="Get all user files info")
async def get_user_files(
    token: str = Depends(reuseable_oauth),
    user_repository: IUserRepository = Depends(get_user_repository),
    file_repository: IFileRepository = Depends(get_file_repository)
    ):
    try:
        files = await get_files(token, user_repository, file_repository)
        results = []
        for file in files:
            results.append(
f"""
"id": {file.id},
"name": {file.name},
"created_ad": {file.created_ad},
"path": {STATIC_DIR}/{file.user_id}/{file.path},
"size": {file.size},
"is_downloadable": {file.is_downloadable}
"""
            )
        return {"message": f"Successfully uploaded {results}"}
    except Exception as e:
        return {"message": f"There was an error uploading the file {e}"}
    
@router.get('/download_file', summary="Download file")
async def download_file(
    path: str,
    filename: str,
    token: str = Depends(reuseable_oauth),
    user_repository: IUserRepository = Depends(get_user_repository),
    file_repository: IFileRepository = Depends(get_file_repository)
    ):
    try:
        path = await get_file_path(token, user_repository, file_repository, path, filename)
        return FileResponse(path=f"{path}{filename}", filename=filename, media_type='multipart/form-data')
    except Exception as e:
        return {"message": f"There was an error uploading the file {e}"}
    