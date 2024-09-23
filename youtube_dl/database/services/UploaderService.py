import re

from youtube_dl.database.DatabaseService import DatabaseService
from youtube_dl.database.models.Uploader import Uploader


class UploaderService(DatabaseService):

    def create_or_get_uploader(self, uploader_name, uploader_id, uploader_url):

        uploader_query = self._session.query(Uploader) \
            .filter(Uploader.uploader_id == uploader_id)

        uploader = uploader_query.one_or_none()

        if uploader is None:
            uploader = Uploader(name=uploader_name, uploader_id=uploader_id, url=uploader_url)
            self._session.add(uploader)

        return uploader

    def create_or_get_uploader_from_info_dict(self, info_dict):
        uploader_name = info_dict.get('uploader', None)
        uploader_id = info_dict.get('uploader_id', None)
        uploader_url = info_dict.get('uploader_url', None)

        if None is uploader_id:
            return None

        return self.create_or_get_uploader(
                uploader_name,
                uploader_id,
                uploader_url
        )
