import re

from youtube_dl.database.DatabaseService import DatabaseService
from youtube_dl.database.models.PlaylistItem import PlaylistItem


class PlaylistItemService(DatabaseService):

    def __init__(self, database_session, playlist_service):
        super().__init__(database_session)
        self.__playlist_service = playlist_service

    def create_or_get_playlist_item(self, playlist_id, name, title, uploader, uploader_id, playlist_index):

        playlist = self.__playlist_service.create_or_get_playlist(playlist_id, name, title, uploader, uploader_id)

        playlist_item_query = self._session.query(PlaylistItem) \
            .filter(PlaylistItem.index == playlist_index and PlaylistItem.playlist == playlist)

        playlist_item = playlist_item_query.one_or_none()

        if playlist_item is None:
            playlist_item = PlaylistItem(index=playlist_index, playlist=playlist)
            self._session.add(playlist_item)

        return playlist_item

    def create_or_get_playlist_item_from_info_dict(self, info_dict):
        playlist = self.__playlist_service.create_or_get_playlist_from_info_dict(info_dict)
        index = info_dict.get('playlist_index', None)

        if None is playlist or index is None:
            return None


        return self.create_or_get_playlist_item(
                playlist.playlist_id,
                playlist.name,
                playlist.title,
                playlist.uploader,
                playlist.uploader_id,
                index
        )
