from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer

from schemas.reference import Reference
from api.dependencies import get_user_repository, get_reference_repository
from services.reference_auth import add_reference_with_auth, get_private_references_with_auth, update_reference_with_auth, get_short_by_original_with_auth, add_batch_reference_with_auth
from repository.i_user_repository import IUserRepository
from repository.i_reference_repository import IReferenceRepository


router = APIRouter()


reuseable_oauth = OAuth2PasswordBearer(
    tokenUrl="v1/login",
    scheme_name="UserAuth"
)


@router.get('/get_public', summary="Return all public references")
async def get_public(reference_repository: IReferenceRepository = Depends(get_reference_repository)):
    try:
        return {
            "references": await reference_repository.get()
        }
    except ValueError as ex:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(ex)
        )
    

@router.get('/get_by_original', summary="Return all short urls by original")
async def get_by_original(
    original_url: str,
    token: str = Depends(reuseable_oauth),
    reference_repository: IReferenceRepository = Depends(get_reference_repository),
    user_repository: IUserRepository = Depends(get_user_repository),
    ):
    try:
        return await get_short_by_original_with_auth(original_url, token, reference_repository, user_repository)
    except ValueError as ex:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(ex)
        )


@router.get('/get_private', summary="Return all private references of user")
async def get_private(
    token: str = Depends(reuseable_oauth),
    reference_repository: IReferenceRepository = Depends(get_reference_repository),
    user_repository: IUserRepository = Depends(get_user_repository),
    ):
    try:
        return await get_private_references_with_auth(token, reference_repository, user_repository)
    except ValueError as ex:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(ex)
        )


@router.post('/add', summary="Create new reference", response_model=Reference)
async def create_reference(
    reference: Reference,
    token: str = Depends(reuseable_oauth),
    reference_repository: IReferenceRepository = Depends(get_reference_repository),
    user_repository: IUserRepository = Depends(get_user_repository),
    ):
    try:
        return await add_reference_with_auth(reference, token, reference_repository, user_repository)
    except ValueError as ex:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(ex)
        )
    

@router.post('/add_batch', summary="Create new references in batch", response_model=list[Reference])
async def create_batch_reference(
    references: list[Reference],
    token: str = Depends(reuseable_oauth),
    reference_repository: IReferenceRepository = Depends(get_reference_repository),
    user_repository: IUserRepository = Depends(get_user_repository),
    ):
    try:
        return await add_batch_reference_with_auth(references, token, reference_repository, user_repository)
    except ValueError as ex:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(ex)
        )

    
@router.post('/update', summary="Update reference by id", response_model=Reference)
async def update(
    reference: Reference,
    token: str = Depends(reuseable_oauth),
    reference_repository: IReferenceRepository = Depends(get_reference_repository),
    user_repository: IUserRepository = Depends(get_user_repository),
    ):
    try:
        return await update_reference_with_auth(reference, token, reference_repository, user_repository)
    except ValueError as ex:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(ex)
        )
