from sqlalchemy import Column, Integer, String, Table, ForeignKey
from sqlalchemy.orm import relationship

from youtube_dl.database import Base


video_info_category = Table(
        'video_info_category', Base.metadata,
        Column('vido_info_id', Integer, ForeignKey('video_info.id'), primary_key=True),
        Column('category_id', Integer, ForeignKey('categories.id'), primary_key=True)
)

class Category(Base):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)

    # Define the relationship, using the association table
    video_infos = relationship('VideoInfo', secondary=video_info_category, back_populates='categories')
