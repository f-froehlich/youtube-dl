from youtube_dl.database.DatabaseService import DatabaseService
from youtube_dl.database.models.Playlist import Playlist


class PlaylistService(DatabaseService):

    def create_or_get_playlist(self, playlist_id, name, title, uploader, uploader_id):

        playlist_query = self._session.query(Playlist) \
            .filter(Playlist.playlist_id == playlist_id)

        playlist = playlist_query.one_or_none()

        if playlist is None:
            playlist = Playlist(
                playlist_id=playlist_id,
                name=name,
                title=title,
                uploader=uploader,
                uploader_id=uploader_id
                )
            self._session.add(playlist)

        return playlist

    def create_or_get_playlist_from_info_dict(self, info_dict):
        playlist_id = info_dict.get('playlist_id', None)
        name = info_dict.get('playlist_name', None)
        title = info_dict.get('playlist_title', None)
        uploader = info_dict.get('playlist_uploader', None)
        uploader_id = info_dict.get('playlist_uploader_id', None)

        if None is playlist_id:
            return None

        return self.create_or_get_playlist(playlist_id, name, title, uploader, uploader_id)
