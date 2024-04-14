from models.d_file import DFile
from db.models.user_file import UserFile


def to_domain_model(model: UserFile) -> DFile:
    return DFile(model.id, model.name, model.path, model.size, model.is_downloadable, model.created_ad, model.user_id)