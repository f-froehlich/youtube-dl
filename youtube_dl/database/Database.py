from sqlalchemy.orm import sessionmaker

from youtube_dl.database import engine, Base
from youtube_dl.database.models.Download import Download
from youtube_dl.database.models.Tag import Tag
from youtube_dl.database.models.VideoInfo import VideoInfo
from youtube_dl.database.services.CategoryService import CategoryService
from youtube_dl.database.services.ChannelService import ChannelService
from youtube_dl.database.services.DownloadableVideoService import DownloadableVideoService
from youtube_dl.database.services.EpisodeService import EpisodeService
from youtube_dl.database.services.ExtractorService import ExtractorService
from youtube_dl.database.services.PlaylistItemService import PlaylistItemService
from youtube_dl.database.services.PlaylistService import PlaylistService
from youtube_dl.database.services.SeasonService import SeasonService
from youtube_dl.database.services.SeriesService import SeriesService
from youtube_dl.database.services.TagService import TagService
from youtube_dl.database.services.UploaderService import UploaderService
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
        self.__playlist_service = PlaylistService(self.__session)
        self.__playlist_item_service = PlaylistItemService(self.__session, self.__playlist_service)
        self.__uploader_service = UploaderService(self.__session)
        self.__channel_service = ChannelService(self.__session)
        self.__tag_service = TagService(self.__session)
        self.__extractor_service = ExtractorService(self.__session)
        self.__category_service = CategoryService(self.__session)
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
        if info_dict['_file_exists']:
            pass
            # return
        episode = self.__episode_service.create_or_get_episode_from_info_dict(info_dict)
        info_dict['_episode'] = episode

        info_dict['_downloadable_videos'] = self.__downloadable_video_service \
            .create_or_get_downloadable_videos_from_info_dict(info_dict)

        info_dict['_channel'] = self.__channel_service \
            .create_or_get_channel_from_info_dict(info_dict)

        info_dict['_uploader'] = self.__uploader_service \
            .create_or_get_uploader_from_info_dict(info_dict)

        info_dict['_playlist_item'] = self.__playlist_item_service \
            .create_or_get_playlist_item_from_info_dict(info_dict)

        info_dict['_tags'] = self.__tag_service \
            .create_or_get_tags_from_info_dict(info_dict)
        info_dict['_categories'] = self.__category_service \
            .create_or_get_categories_from_info_dict(info_dict)
        info_dict['_extractor'] = self.__extractor_service \
            .create_or_get_extractor_from_info_dict(info_dict)

        video_info_query = self.__session.query(VideoInfo) \
            .filter(VideoInfo.webpage_url == info_dict['webpage_url'])

        video_info = video_info_query.one_or_none()
        if None is video_info:
            video_info = VideoInfo(**info_dict)
            self.__session.add(video_info)
        else:
            video_info.episode = episode
            video_info.downloadable_videos.extend(info_dict['_downloadable_videos'])

        for format_dict in info_dict.get('__downloaded_formats', []):
            for downloadable_video in video_info.downloadable_videos:
                if (downloadable_video.url == format_dict.get('url')
                        and downloadable_video.format.format_id == format_dict['format_id']):
                    download = Download(
                            filepath=format_dict['_filename'],
                            video_info=video_info,
                            downloadable_video=downloadable_video,
                            tbr=format_dict.get('tbr', None),
                            abr=format_dict.get('abr', None),
                            acodec=format_dict.get('acodec', None),
                            asr=format_dict.get('asr', None),
                            vbr=format_dict.get('vbr', None),
                            fps=format_dict.get('fps', None),
                            vcodec=format_dict.get('vcodec', None),
                            container=format_dict.get('container', None),
                            filesize=format_dict.get('filesize', None),
                            filesize_approx=format_dict.get('filesize_approx', None),
                            protocol=format_dict.get('protocol', None),
                            epoch=format_dict.get('epoch', None),
                            autonumber=format_dict.get('autonumber', None),
                    )
                    self.__session.add(download)
                    break
        for downloadable_video in video_info.downloadable_videos:
            download = Download(
                    filepath=f"{info_dict['_filename']}",
                    video_info=video_info,
                    downloadable_video=downloadable_video,
                    tbr=info_dict.get('tbr', None),
                    abr=info_dict.get('abr', None),
                    acodec=info_dict.get('acodec', None),
                    asr=info_dict.get('asr', None),
                    vbr=info_dict.get('vbr', None),
                    fps=info_dict.get('fps', None),
                    vcodec=info_dict.get('vcodec', None),
                    container=info_dict.get('container', None),
                    filesize=info_dict.get('filesize', None),
                    filesize_approx=info_dict.get('filesize_approx', None),
                    protocol=info_dict.get('protocol', None),
                    epoch=info_dict.get('epoch', None),
                    autonumber=info_dict.get('autonumber', None),
            )
            self.__session.add(download)
            break

        return video_info
