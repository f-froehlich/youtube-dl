from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from youtube_dl.database import Base


class Thumbnail(Base):
    __tablename__ = 'thumbnails'

    id = Column(Integer, primary_key=True)
    url = Column(String, nullable=True)
    thumbnail_id = Column(String, nullable=True)

    video_info_id = Column(Integer, ForeignKey('video_info.id'))
    video_info = relationship('VideoInfo', back_populates='thumbnails')

    def __init__(self, *args, **kwargs):
        """
        Constructor that sets properties if they exist in kwargs.
        """
        for key, value in kwargs.items():
            if hasattr(self, key):
                if 'id' == key:
                    self.thumbnail_id = value
                else:
                    setattr(self, key, value)
