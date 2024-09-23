from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship

from youtube_dl.database import Base
from youtube_dl.database.models.Season import Season
from youtube_dl.database.models.VideoInfo import VideoInfo


class Episode(Base):
    __tablename__ = 'episodes'
    __table_args__ = (
        UniqueConstraint('season_id', 'episode_number', name='season_episode_constraint'),
    )

    id = Column(Integer, primary_key=True)
    episode_number = Column(Integer, nullable=False)
    episode_name = Column(String, nullable=False)

    season_id = Column(Integer, ForeignKey('seasons.id'))
    season = relationship(Season, back_populates='episodes')

    video_infos = relationship(VideoInfo, back_populates='episode')


