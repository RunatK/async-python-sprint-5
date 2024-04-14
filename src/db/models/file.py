import datetime
import pathlib

from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime
from sqlalchemy.orm import Mapped, relationship, mapped_column

from .base import Base
    


class File(Base):
    __tablename__ = "files"

    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    path = Column(String)
    size = Column(Integer)
    is_downloadable = Column(Boolean, default=False)
    created_ad = Column(DateTime, default=datetime.datetime.now())
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped["User"] = relationship(lazy="joined")

    def __repr__(self) -> str:
        full_path = pathlib.Path()
        return str(full_path.joinpath(self.path, self.name))
    
    def __str__(self):
        full_path = pathlib.Path()
        return str(full_path.joinpath(self.path, self.name))
    