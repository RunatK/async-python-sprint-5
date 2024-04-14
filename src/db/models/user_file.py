import datetime

from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime
from sqlalchemy.orm import Mapped, relationship, mapped_column

from .base import Base


class UserFile(Base):
    __tablename__ = "ufiles"

    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    path = Column(String)
    size = Column(Integer)
    is_downloadable = Column(Boolean)
    created_ad = Column(DateTime)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    def __repr__(self) -> str:
        return str(self.id)
    
    