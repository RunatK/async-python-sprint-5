from models.d_file import DFile
from db.models.file import File


def to_domain_model(model: File) -> DFile:
    return DFile(model.id, model.name, model.path, model.size, model.is_downloadable, model.created_ad, model.user_id)