from typing import Optional

from fastapi import APIRouter, Depends, UploadFile, File
from fastapi.security import OAuth2PasswordBearer

from api.dependencies import get_user_repository
from repository.i_user_repository import IUserRepository
from services.file_auth import file_upload

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
    user_repository: IUserRepository = Depends(get_user_repository)
    ):
    result = {}
    try:
        contents = file.file.read()
        result = await file_upload(token, user_repository, contents, dir_path, file.filename)
    except Exception as e:
        result = {"message": f"There was an error uploading the file {e}"}
        raise e
    finally:
        file.file.close()
    return result