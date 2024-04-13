from models.d_reference import DReference
from repository.i_reference_repository import AddReferenceDTO, UpdateReferenceDTO, IReferenceRepository
from repository.i_user_repository import IUserRepository
from schemas.reference import Reference
from services.logon import UserLogon


async def add_reference_with_auth(
    reference: Reference,
    token: str,
    reference_repository: IReferenceRepository,
    user_repository: IUserRepository) -> Reference:
    """
    Создание ссылки с авторизацией
    """
    logon = UserLogon()
    user = await logon.autherization(token, user_repository)
    dto = AddReferenceDTO(
        reference.short_id,
        reference.short_url,
        reference.original_url,
        reference.visibility.name,
        user_id=user.id
    )
    await reference_repository.add(dto)
    return reference


async def add_batch_reference_with_auth(
    references: list[Reference],
    token: str,
    reference_repository: IReferenceRepository,
    user_repository: IUserRepository) -> Reference:
    """
    Создание ссылок с авторизацией
    """
    logon = UserLogon()
    user = await logon.autherization(token, user_repository)
    dtos: list[AddReferenceDTO] = []
    for reference in references:
        dtos.append(AddReferenceDTO(
            reference.short_id,
            reference.short_url,
            reference.original_url,
            reference.visibility.name,
            user_id=user.id
        ))
    await reference_repository.add_batch_references(dtos)
    return references


async def get_private_references_with_auth(
    token: str,
    reference_repository: IReferenceRepository,
    user_repository: IUserRepository
    ) -> dict[str, list[DReference]]:
    """
    Получение всех ссылок пользователя с авторизацией
    """
    logon = UserLogon()
    user = await logon.autherization(token, user_repository)
    return {
        "references": await reference_repository.get_by_user_id(user.id)
    }

async def get_short_by_original_with_auth(
    original_url: str,
    token: str,
    reference_repository: IReferenceRepository,
    user_repository: IUserRepository
    ) -> dict[str, list[DReference]]:
    """
    
    """
    logon = UserLogon()
    user = await logon.autherization(token, user_repository)
    return {
        "references": await reference_repository.get_short_urls_by_original(original_url, user.id)
    }

async def update_reference_with_auth(
    reference: Reference,
    token: str,
    reference_repository: IReferenceRepository,
    user_repository: IUserRepository    
    ) -> Reference:
    """
    
    """
    logon = UserLogon()
    user = await logon.autherization(token, user_repository)
    dto = UpdateReferenceDTO(
        reference.short_id,
        reference.short_url,
        reference.original_url,
        reference.visibility,
        user_id=user.id
    )
    await reference_repository.update(dto)
    return reference

