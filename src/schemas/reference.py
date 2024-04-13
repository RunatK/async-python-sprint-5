from enum import Enum

from pydantic import BaseModel

from models.d_reference import VisibilityType

class Reference(BaseModel):
    short_id: str
    short_url: str
    original_url: str
    visibility: VisibilityType