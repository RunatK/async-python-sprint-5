from fastapi import APIRouter, Depends
from api.dependencies import get_status

router = APIRouter()

@router.get('/ping', summary="Return db status")
def get_status(
    status: str = Depends(get_status)
    ):
    return status