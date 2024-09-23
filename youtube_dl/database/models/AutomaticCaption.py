from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from youtube_dl.database import Base


class AutomaticCaption(Base):
    __tablename__ = 'automatic_captions'

    id = Column(Integer, primary_key=True)
    url = Column(String, nullable=False)
    ext = Column(String, nullable=False)
    locale = Column(String, nullable=False)
    content = Column(String, nullable=True)

    video_info_id = Column(Integer, ForeignKey('video_info.id'))
    video_info = relationship('VideoInfo', back_populates='automatic_captions')

    def __init__(self, *args, **kwargs):
        """
        Constructor that sets properties if they exist in kwargs.
        """
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
