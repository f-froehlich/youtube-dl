from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship

from youtube_dl.database import Base
from youtube_dl.database.models.Download import Download


class DownloadableVideo(Base):
    __tablename__ = 'downloadable_video'

    id = Column(Integer, primary_key=True)
    url = Column(String, nullable=True, unique=True)
    ext = Column(String, nullable=True)

    video_info_id = Column(Integer, ForeignKey('video_info.id'))
    video_info = relationship('VideoInfo', back_populates='downloadable_videos')

    format_id = Column(Integer, ForeignKey('video_formats.id'))
    format = relationship('VideoFormat', back_populates='downloadable_videos')

    downloads = relationship(Download, back_populates='downloadable_video')




