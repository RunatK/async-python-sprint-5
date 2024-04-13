from typing import List

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import Mapped, relationship

from .reference import Reference
from .base import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    login = Column(String, unique=True)
    password = Column(String)
    references: Mapped[List["Reference"]] = relationship(back_populates="user", lazy='joined', uselist=True)

    def __repr__(self) -> str:
        return str(self.id)