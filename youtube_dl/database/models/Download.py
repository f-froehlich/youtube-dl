from sqlalchemy import Column, Integer, String, ForeignKey, Float
from sqlalchemy.orm import relationship

from youtube_dl.database import Base


class Download(Base):
    __tablename__ = 'downloads'

    id = Column(Integer, primary_key=True)
    filepath = Column(String, nullable=False)

    tbr = Column(Float, nullable=True)
    abr = Column(Float, nullable=True)
    acodec = Column(String, nullable=True)
    asr = Column(Float, nullable=True)
    vbr = Column(Float, nullable=True)
    fps = Column(Float, nullable=True)
    vcodec = Column(String, nullable=True)
    container = Column(String, nullable=True)
    filesize = Column(Float, nullable=True)
    filesize_approx = Column(Float, nullable=True)
    protocol = Column(String, nullable=True)
    epoch = Column(Float, nullable=True)
    autonumber = Column(Float, nullable=True)



    video_info_id = Column(Integer, ForeignKey('video_info.id'))
    video_info = relationship('VideoInfo', back_populates='downloads')

    downloadable_video_id = Column(Integer, ForeignKey('downloadable_video.id'))
    downloadable_video = relationship('DownloadableVideo', back_populates='downloads')
