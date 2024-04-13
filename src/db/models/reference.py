import uuid
from enum import Enum as PyEnum

from sqlalchemy import Column, Integer, String, ForeignKey, Enum
from sqlalchemy.orm import Mapped, relationship, mapped_column

from .base import Base
    
VisibilityType = PyEnum(
    value='VisibilityType',
    names=('private', 'public')
)
    


class Reference(Base):
    __tablename__ = "references"

    id = Column(Integer, primary_key=True)
    short_id = Column(String(255), unique=True)
    short_url = Column(String)
    original_url = Column(String)
    visibility = Column(Enum(VisibilityType))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped["User"] = relationship(back_populates="references", lazy="joined")

    def __repr__(self) -> str:
        return str(self.short_id)