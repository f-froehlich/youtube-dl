from sqlalchemy import Column, Integer, String, Table, ForeignKey
from sqlalchemy.orm import relationship

from youtube_dl.database import Base


video_info_tag = Table(
        'video_info_tag', Base.metadata,
        Column('vido_info_id', Integer, ForeignKey('video_info.id'), primary_key=True),
        Column('tag_id', Integer, ForeignKey('tags.id'), primary_key=True)
)

class Tag(Base):
    __tablename__ = 'tags'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)

    # Define the relationship, using the association table
    video_infos = relationship('VideoInfo', secondary=video_info_tag, back_populates='tags')
