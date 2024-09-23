import json

from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from youtube_dl.database import Base
from youtube_dl.database.models.AutomaticCaption import AutomaticCaption
from youtube_dl.database.models.Category import Category, video_info_category
from youtube_dl.database.models.Channel import Channel
from youtube_dl.database.models.Download import Download
from youtube_dl.database.models.Subtitle import Subtitle
from youtube_dl.database.models.Tag import Tag, video_info_tag
from youtube_dl.database.models.Thumbnail import Thumbnail
from youtube_dl.database.models.DownloadableVideo import DownloadableVideo
from youtube_dl.database.models.Uploader import Uploader


class VideoInfo(Base):
    __tablename__ = 'video_info'

    # Defining columns for all properties with nullable=True
    id = Column(Integer, primary_key=True)
    webpage_url = Column(String, nullable=False, unique=True)
    video_id = Column(String, nullable=True)
    title = Column(String, nullable=True)
    alt_title = Column(String, nullable=True)
    display_id = Column(String, nullable=True)
    license = Column(String, nullable=True)
    creator = Column(String, nullable=True)
    release_date = Column(String, nullable=True)
    timestamp = Column(Float, nullable=True)
    upload_date = Column(String, nullable=True)
    location = Column(String, nullable=True)
    duration = Column(Float, nullable=True)
    view_count = Column(Float, nullable=True)
    like_count = Column(Float, nullable=True)
    dislike_count = Column(Float, nullable=True)
    repost_count = Column(Float, nullable=True)
    average_rating = Column(Float, nullable=True)
    comment_count = Column(Float, nullable=True)
    age_limit = Column(Integer, nullable=True)
    is_live = Column(Boolean, nullable=True)
    start_time = Column(Float, nullable=True)
    end_time = Column(Float, nullable=True)
    thumbnail = Column(String, nullable=True)
    description = Column(String, nullable=True)
    fulltitle = Column(String, nullable=True)

# TODO -->
#     chapter = Column(String, nullable=True)
#     chapter_number = Column(Float, nullable=True)
#     chapter_id = Column(String, nullable=True)
#     track = Column(String, nullable=True)
#     track_number = Column(Float, nullable=True)
#     track_id = Column(String, nullable=True)
#     artist = Column(String, nullable=True)
#     genre = Column(String, nullable=True)
#     album = Column(String, nullable=True)
#     album_type = Column(String, nullable=True)
#     album_artist = Column(String, nullable=True)
#     disc_number = Column(Float, nullable=True)
# <-- END TODO

    release_year = Column(Float, nullable=True)
    manifest_url = Column(String, nullable=True)

    download_store = relationship('DownloadStore', back_populates='video_info')
    downloadable_videos = relationship(DownloadableVideo, back_populates='video_info')
    thumbnails = relationship(Thumbnail, back_populates='video_info')
    subtitles = relationship(Subtitle, back_populates='video_info')
    automatic_captions = relationship(AutomaticCaption, back_populates='video_info')
    downloads = relationship(Download, back_populates='video_info')

    episode_id = Column(Integer, ForeignKey('episodes.id'))  # Corrected ForeignKey reference
    episode = relationship('Episode', back_populates='video_infos')

    playlist_item_id = Column(Integer, ForeignKey('playlist_items.id'))  # Corrected ForeignKey reference
    playlist_item = relationship('PlaylistItem', back_populates='video_infos')

    channel_id = Column(Integer, ForeignKey('channels.id'))  # Corrected ForeignKey reference
    channel = relationship(Channel, back_populates='video_info')

    uploader_id = Column(Integer, ForeignKey('uploaders.id'))  # Corrected ForeignKey reference
    uploader = relationship(Uploader, back_populates='video_info')

    extractor_id = Column(Integer, ForeignKey('extractors.id'))  # Corrected ForeignKey reference
    extractor = relationship('Extractor', back_populates='video_info')


    tags = relationship(Tag, secondary=video_info_tag, back_populates='video_infos')
    categories = relationship(Category, secondary=video_info_category, back_populates='video_infos')


    def __init__(self, *args, **kwargs):
        """
        Constructor that sets properties if they exist in kwargs.
        """
        for key, value in kwargs.items():
            if hasattr(self, key):

                if 'id' == key:
                    self.video_id = value
                elif 'thumbnails' == key:
                    self.thumbnails = [Thumbnail(**i) for i in value]
                elif 'subtitles' == key:
                    self.subtitles = []
                    for locale, captions in value.items():
                        self.subtitles.extend(
                                [Subtitle(locale=locale, **caption) for caption in captions]
                                )
                elif key in ["episode", "channel", "uploader", "tags", "categories", "extractor"]:
                    pass
                elif 'automatic_captions' == key:
                    self.automatic_captions = []
                    for locale, captions in value.items():
                        self.automatic_captions.extend([AutomaticCaption(locale=locale, **caption) for caption in captions])
                elif 'categories' == key:
                    self.categories = json.dumps(value)
                else:
                    setattr(self, key, value)
            elif '_episode' == key:
                self.episode = value
            elif '_downloadable_videos' == key:
                self.downloadable_videos = value
            elif '_channel' == key:
                self.channel = value
            elif '_uploader' == key:
                self.uploader = value
            elif '_playlist_item' == key:
                self.playlist_item = value
            elif '_tags' == key:
                self.tags = value
            elif '_categories' == key:
                self.categories = value
            elif '_extractor' == key:
                self.extractor = value
            else:
                print(key, False, type(value))
