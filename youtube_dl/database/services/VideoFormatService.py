import re

from youtube_dl.database.DatabaseService import DatabaseService
from youtube_dl.database.models.VideoFormat import VideoFormat


class VideoFormatService(DatabaseService):

    def create_or_get_video_format(self, format_id, format_name):
        video_format_query = self._session.query(VideoFormat).filter(VideoFormat.format_id == format_id)
        video_format = video_format_query.one_or_none()
        if None is video_format:
            width = height = None
            resolution_match = re.search(r"(\d+)x(\d+)", format_name)
            if resolution_match:
                width = int(resolution_match.group(1))
                height = int(resolution_match.group(2))

            video_format = VideoFormat(
                    format_id=format_id,
                    format_name=format_name,
                    width=width,
                    height=height
            )
            self._session.add(video_format)
        return video_format

    def create_or_get_video_format_from_format_dict(self, format_dict):

        return self.create_or_get_video_format(format_dict['format_id'], format_dict['format'])
