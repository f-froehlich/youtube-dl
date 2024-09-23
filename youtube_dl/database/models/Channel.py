from sqlalchemy import Column, Integer, String, ForeignKey, Float, Boolean
from sqlalchemy.orm import relationship

from youtube_dl.database import Base


class Channel(Base):
    __tablename__ = 'channels'

    id = Column(Integer, primary_key=True)
    channel_id = Column(String, nullable=False, unique=True)
    url = Column(String, nullable=False)
    name = Column(Integer, nullable=False)

    video_info = relationship('VideoInfo', back_populates='channel')







