from repository.i_user_repository import IUserRepository
from db.repository.user_repository import UserRepository
from repository.i_reference_repository import IReferenceRepository
from db.repository.reference_repository import ReferenceRepository
from services.ping_servers import servers_ping


def get_user_repository() -> IUserRepository: 
    return UserRepository()

def get_reference_repository() -> IReferenceRepository:
    return ReferenceRepository()

def get_status() -> str:
    return servers_ping()
