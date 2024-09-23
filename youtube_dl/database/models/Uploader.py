from sqlalchemy import Column, Integer, String, ForeignKey, Float, Boolean
from sqlalchemy.orm import relationship

from youtube_dl.database import Base


class Uploader(Base):
    __tablename__ = 'uploaders'

    id = Column(Integer, primary_key=True)
    uploader_id = Column(String, nullable=False, unique=True)
    url = Column(String, nullable=False)
    name = Column(Integer, nullable=False)

    video_info = relationship('VideoInfo', back_populates='uploader')







