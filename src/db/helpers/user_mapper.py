from sqlalchemy.exc import MissingGreenlet

from models.d_user import DUser
from db.models.user import User as DBUser
from db.helpers.reference_mapper import to_domain_model as reference_mapper


def to_domain_model(model: DBUser) -> DUser:
    try:
        return DUser(model.id, model.login, model.password)
    except MissingGreenlet:
        return DUser(model.id, model.login, model.password)
