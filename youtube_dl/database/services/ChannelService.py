import re

from youtube_dl.database.DatabaseService import DatabaseService
from youtube_dl.database.models.Channel import Channel


class ChannelService(DatabaseService):

    def create_or_get_channel(self, channel_name, channel_id, channel_url):

        channel_query = self._session.query(Channel) \
            .filter(Channel.channel_id == channel_id)

        channel = channel_query.one_or_none()

        if channel is None:
            channel = Channel(name=channel_name, channel_id=channel_id, url=channel_url)
            self._session.add(channel)

        return channel

    def create_or_get_channel_from_info_dict(self, info_dict):
        channel_name = info_dict.get('channel', None)
        channel_id = info_dict.get('channel_id', None)
        channel_url = info_dict.get('channel_url', None)

        if None is channel_id:
            return None

        return self.create_or_get_channel(
                channel_name,
                channel_id,
                channel_url
        )
