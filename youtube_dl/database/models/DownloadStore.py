from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from youtube_dl.database import Base
from youtube_dl.database.models.VideoInfo import VideoInfo


class DownloadStore(Base):
    __tablename__ = 'downloads'

    id = Column(Integer, primary_key=True)
    url = Column(String, nullable=False)
    data = Column(String)  # JSON string

    # Foreign Key - references id in VideoInfo
    video_info_id = Column(String, ForeignKey('video_info.id'))

    # Relationship with VideoInfo
    video_info = relationship(VideoInfo, back_populates='download_store')

