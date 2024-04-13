from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from schemas.user import UserAuth
from schemas.token import TokenSchema
from api.dependencies import get_user_repository
from services.logon import UserLogon
from repository.i_user_repository import AddUserDTO, IUserRepository

router = APIRouter()

@router.post('/signup', summary="Create new user", response_model=UserAuth)
async def create_user(data: UserAuth, user_repository: IUserRepository = Depends(get_user_repository)):
    # querying database to check if user already exist
    try:
        logon = UserLogon()
        add_user_dto = AddUserDTO(data.login, data.password)
        await logon.registration(add_user_dto, user_repository)
        return data
    except ValueError as ex:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(ex)
        )
    

@router.post('/login', summary="Create access and refresh tokens for user", response_model=TokenSchema)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), user_repository: IUserRepository = Depends(get_user_repository)):
    try:
        logon = UserLogon()
        return await logon.authentication(form_data.username, form_data.password, user_repository)
    except ValueError as ex:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(ex)
        )
