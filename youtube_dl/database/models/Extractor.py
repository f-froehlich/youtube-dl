from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from youtube_dl.database import Base


class Extractor(Base):
    __tablename__ = 'extractors'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    extractor_key = Column(String, nullable=False, unique=True)

    video_info = relationship('VideoInfo', back_populates='extractor')

