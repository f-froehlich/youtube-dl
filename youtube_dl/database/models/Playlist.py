from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship

from youtube_dl.database import Base
from youtube_dl.database.models.Series import Series


class Playlist(Base):
    __tablename__ = 'playlists'

    id = Column(Integer, primary_key=True)

    playlist_id = Column(String, nullable=False, unique=True)
    name = Column(String, nullable=True)
    title = Column(String, nullable=True)
    uploader = Column(String, nullable=True)
    uploader_id = Column(String, nullable=True)

    items = relationship('PlaylistItem', back_populates='playlist')




