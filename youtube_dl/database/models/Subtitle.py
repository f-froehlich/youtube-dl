from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from youtube_dl.database import Base


class Subtitle(Base):
    __tablename__ = 'subtitles'

    id = Column(Integer, primary_key=True)
    url = Column(String, nullable=True)
    ext = Column(String, nullable=True)
    locale = Column(String, nullable=True)

    video_info_id = Column(Integer, ForeignKey('video_info.id'))
    video_info = relationship('VideoInfo', back_populates='subtitles')

    def __init__(self, *args, **kwargs):
        """
        Constructor that sets properties if they exist in kwargs.
        """
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
