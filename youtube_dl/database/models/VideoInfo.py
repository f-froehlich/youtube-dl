import json

from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from youtube_dl.database import Base
from youtube_dl.database.models.AutomaticCaption import AutomaticCaption
from youtube_dl.database.models.Subtitle import Subtitle
from youtube_dl.database.models.Thumbnail import Thumbnail
from youtube_dl.database.models.DownloadableVideo import DownloadableVideo


class VideoInfo(Base):
    __tablename__ = 'video_info'

    # Defining columns for all properties with nullable=True
    id = Column(Integer, primary_key=True)
    video_id = Column(String, nullable=True)
    title = Column(String, nullable=True)
    ext = Column(String, nullable=True)
    alt_title = Column(String, nullable=True)
    display_id = Column(String, nullable=True)
    uploader = Column(String, nullable=True)
    license = Column(String, nullable=True)
    creator = Column(String, nullable=True)
    release_date = Column(String, nullable=True)
    timestamp = Column(Float, nullable=True)
    upload_date = Column(String, nullable=True)
    uploader_id = Column(String, nullable=True)
    channel = Column(String, nullable=True)
    channel_id = Column(String, nullable=True)
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
    webpage_url = Column(String, nullable=True)
    webpage_url_basename = Column(String, nullable=True)
    uploader_url = Column(String, nullable=True)
    channel_url = Column(String, nullable=True)
    thumbnail = Column(String, nullable=True)
    description = Column(String, nullable=True)
    fulltitle = Column(String, nullable=True)
    filename = Column(String, nullable=True)
    # format = Column(String, nullable=True)
    # format_id = Column(String, nullable=True)
    # format_note = Column(String, nullable=True)
    # width = Column(Integer, nullable=True)
    # height = Column(Integer, nullable=True)
    # resolution = Column(String, nullable=True)
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
    extractor = Column(String, nullable=True)
    extractor_key = Column(String, nullable=True)
    epoch = Column(Float, nullable=True)
    autonumber = Column(Float, nullable=True)
    playlist = Column(String, nullable=True)
    playlist_index = Column(Float, nullable=True)
    playlist_id = Column(String, nullable=True)
    playlist_title = Column(String, nullable=True)
    playlist_uploader = Column(String, nullable=True)
    playlist_uploader_id = Column(String, nullable=True)
    chapter = Column(String, nullable=True)
    chapter_number = Column(Float, nullable=True)
    chapter_id = Column(String, nullable=True)
    # series = Column(String, nullable=True)
    # season = Column(String, nullable=True)
    # season_number = Column(Float, nullable=True)
    # season_id = Column(String, nullable=True)
    # episode = Column(String, nullable=True)
    # episode_number = Column(Float, nullable=True)
    # episode_id = Column(String, nullable=True)
    track = Column(String, nullable=True)
    track_number = Column(Float, nullable=True)
    track_id = Column(String, nullable=True)
    artist = Column(String, nullable=True)
    genre = Column(String, nullable=True)
    album = Column(String, nullable=True)
    album_type = Column(String, nullable=True)
    album_artist = Column(String, nullable=True)
    disc_number = Column(Float, nullable=True)
    release_year = Column(Float, nullable=True)
    categories = Column(String, nullable=True)
    tags = Column(String, nullable=True)
    manifest_url = Column(String, nullable=True)

    download_store = relationship('DownloadStore', back_populates='video_info')
    downloadable_videos = relationship(DownloadableVideo, back_populates='video_info')
    thumbnails = relationship(Thumbnail, back_populates='video_info')
    subtitles = relationship(Subtitle, back_populates='video_info')
    automatic_captions = relationship(AutomaticCaption, back_populates='video_info')

    # episode_id = Column(Integer, ForeignKey('episode.id'))
    # episode = relationship('Episode', back_populates='video_infos')

    episode_id = Column(Integer, ForeignKey('episodes.id'))  # Corrected ForeignKey reference
    episode = relationship('Episode', back_populates='video_infos')




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
                elif 'episode' == key:
                    pass
                elif 'automatic_captions' == key:
                    self.automatic_captions = []
                    for locale, captions in value.items():
                        self.automatic_captions.extend([AutomaticCaption(locale=locale, **caption) for caption in captions])
                elif 'categories' == key:
                    self.categories = json.dumps(value)
                elif 'tags' == key:
                    self.tags = json.dumps(value)
                else:
                    setattr(self, key, value)
            elif '_filename' == key:
                self.filename = value
            elif '_episode' == key:
                self.episode = value
            elif '_downloadable_videos' == key:
                self.downloadable_videos = value
            else:
                print(key, False, type(value))
