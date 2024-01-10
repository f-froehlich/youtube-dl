import re

from youtube_dl.database.DatabaseService import DatabaseService
from youtube_dl.database.models.Episode import Episode


class EpisodeService(DatabaseService):

    def __init__(self, database_session, season_service):
        super().__init__(database_session)
        self.__season_service = season_service

    def create_or_get_episode(self, series_name, season_name, season_number, episode_name, episode_number):

        season = self.__season_service.create_or_get_season(series_name, season_name, season_number)

        episode_query = self._session.query(Episode) \
            .filter(Episode.episode_name == episode_name and Episode.season == season)

        episode = episode_query.one_or_none()

        if episode is None:
            episode = Episode(episode_number=episode_number, episode_name=episode_name, season=season)
            self._session.add(episode)

        return episode

    def create_or_get_episode_from_info_dict(self, info_dict):
        season = self.__season_service.create_or_get_season_from_info_dict(info_dict)
        episode_name = info_dict.get('episode', None)
        episode_number = info_dict.get('episode_number', None)

        if None is season:
            return None

        if None is episode_name and None is episode_number:
            return None
        elif None is episode_number and None is not episode_name:
            episode_match = re.search(r"(\d+)", episode_name)
            if episode_match:
                episode_number = int(episode_match.group(1))
            else:
                episode_number = 0
        else:
            episode_name = f"Episode {episode_number}"

        return self.create_or_get_episode(
                season.series.name,
                season.season_name,
                season.season_number,
                episode_name,
                episode_number
        )
