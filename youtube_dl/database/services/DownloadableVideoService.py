from youtube_dl.database.DatabaseService import DatabaseService
from youtube_dl.database.models.DownloadableVideo import DownloadableVideo


class DownloadableVideoService(DatabaseService):

    def __init__(self, database_session, video_format_service):
        super().__init__(database_session)
        self.__video_format_service = video_format_service

    def create_or_get_downloadable_video(self, url, ext, video_format):
        downloadable_video_query = self._session.query(DownloadableVideo) \
            .filter(DownloadableVideo.url == url)

        downloadable_video = downloadable_video_query.one_or_none()
        if None is downloadable_video:
            downloadable_video = DownloadableVideo(
                    url=url,
                    ext=ext,
                    format=video_format,
            )
            self._session.add(downloadable_video)
        return downloadable_video

    def create_or_get_downloadable_videos_from_info_dict(self, info_dict):
        return [
                self.create_or_get_downloadable_video(
                        format_dict['url'],
                        format_dict['ext'],
                        self.__video_format_service.create_or_get_video_format_from_format_dict(format_dict)
                )
                for format_dict in info_dict['formats']
        ]
