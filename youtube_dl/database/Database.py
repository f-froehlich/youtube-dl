from sqlalchemy.orm import sessionmaker

from youtube_dl.database import engine, Base
from youtube_dl.database.models.VideoInfo import VideoInfo
from youtube_dl.database.services.DownloadableVideoService import DownloadableVideoService
from youtube_dl.database.services.EpisodeService import EpisodeService
from youtube_dl.database.services.SeasonService import SeasonService
from youtube_dl.database.services.SeriesService import SeriesService
from youtube_dl.database.services.VideoFormatService import VideoFormatService


class Database:

    __session = None

    def __init__(self):
        # Create a Session class with this engine
        Base.metadata.create_all(engine)
        session = sessionmaker(bind=engine)

        # Instantiate a session
        self.__session = session()
        self.__video_format_service = VideoFormatService(self.__session)
        self.__downloadable_video_service = DownloadableVideoService(self.__session, self.__video_format_service)
        self.__series_service = SeriesService(self.__session)
        self.__season_service = SeasonService(self.__session, self.__series_service)
        self.__episode_service = EpisodeService(self.__session, self.__season_service)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.commit()

    def get_session(self):
        return self.__session

    def commit(self):
        self.__session.commit()

    def get_series_service(self):
        return self.__series_service

    def get_season_service(self):
        return self.__season_service

    def get_episode_service(self):
        return self.__episode_service

    def get_video_format_service(self):
        return self.__video_format_service

    def get_downloadable_video_service(self):
        return self.__downloadable_video_service

    def create_video_info_from_info_dict(self, info_dict):
        episode = self.__episode_service.create_or_get_episode_from_info_dict(info_dict)
        info_dict['_episode'] = episode

        info_dict['_downloadable_videos'] = self.__downloadable_video_service\
            .create_or_get_downloadable_videos_from_info_dict(info_dict)

        video_info = VideoInfo(**info_dict)
        self.__session.add(video_info)

        return video_info
