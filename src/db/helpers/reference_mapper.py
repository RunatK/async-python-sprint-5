from models.d_reference import DReference
from db.models.reference import Reference


def to_domain_model(model: Reference) -> DReference:
    return DReference(model.id, model.short_id, model.short_url, model.original_url, model.visibility, model.user_id)