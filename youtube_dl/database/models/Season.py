from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship

from youtube_dl.database import Base
from youtube_dl.database.models.Series import Series


class Season(Base):
    __tablename__ = 'seasons'

    __table_args__ = (
        UniqueConstraint('series_id', 'season_number', name='series_season_constraint'),
    )

    id = Column(Integer, primary_key=True)
    season_number = Column(Integer, nullable=False)
    season_name = Column(String, nullable=False)

    series_id = Column(Integer, ForeignKey('series.id'))
    series = relationship(Series, back_populates='seasons')

    # This will hold the relationship to VideoInfo
    # video_infos = relationship(VideoInfo, back_populates='season')

    episodes = relationship('Episode', back_populates='season')




