from sqlalchemy import Column, Integer, String, ForeignKey, Float, Boolean
from sqlalchemy.orm import relationship

from youtube_dl.database import Base


class VideoFormat(Base):
    __tablename__ = 'video_formats'

    id = Column(Integer, primary_key=True)
    format_id = Column(String, nullable=False, unique=True)
    format_name = Column(String, nullable=False)
    width = Column(Integer, nullable=True)
    height = Column(Integer, nullable=True)

    # Relationship to DownloadableVideo (one to many)
    downloadable_videos = relationship('DownloadableVideo', back_populates='format')







