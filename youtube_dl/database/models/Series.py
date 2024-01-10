from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from youtube_dl.database import Base


class Series(Base):
    __tablename__ = 'series'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    description = Column(String, nullable=True)

    seasons = relationship('Season', back_populates='series')



