from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship

from youtube_dl.database import Base
from youtube_dl.database.models.Playlist import Playlist
from youtube_dl.database.models.Season import Season
from youtube_dl.database.models.VideoInfo import VideoInfo


class PlaylistItem(Base):
    __tablename__ = 'playlist_items'
    __table_args__ = (
        UniqueConstraint('index', 'playlist_id', name='playlist_id_index'),
    )

    id = Column(Integer, primary_key=True)
    index = Column(Integer, nullable=False)

    playlist_id = Column(Integer, ForeignKey('playlists.id'))
    playlist = relationship(Playlist, back_populates='items')

    video_infos = relationship(VideoInfo, back_populates='playlist_item')


