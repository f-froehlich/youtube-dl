from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from youtube_dl.database import Base


class Subtitle(Base):
    __tablename__ = 'subtitles'

    id = Column(Integer, primary_key=True)
    url = Column(String, nullable=False)
    ext = Column(String, nullable=False)
    locale = Column(String, nullable=False)
    content = Column(String, nullable=True)

    video_info_id = Column(Integer, ForeignKey('video_info.id'))
    video_info = relationship('VideoInfo', back_populates='subtitles')
