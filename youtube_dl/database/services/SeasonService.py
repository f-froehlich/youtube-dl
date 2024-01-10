import re

from youtube_dl.database.DatabaseService import DatabaseService
from youtube_dl.database.models.Season import Season


class SeasonService(DatabaseService):

    def __init__(self, database_session, series_service):
        super().__init__(database_session)
        self.__series_service = series_service

    def create_or_get_season(self, series_name, season_name, season_number):
        series = self.__series_service.create_or_get_series(series_name)

        season_query = self._session.query(Season) \
            .filter(Season.season_name == season_name and Season.series == series)

        season = season_query.one_or_none()

        if season is None:
            season = Season(season_number=season_number, season_name=season_name, series=series)
            self._session.add(season)

        return season

    def create_or_get_season_from_info_dict(self, info_dict):
        season_number = info_dict.get('season_number', None)
        season_name = info_dict.get('season', None)
        series_name = info_dict.get('series', None)

        if None is series_name:
            return None

        if None is season_number and None is season_name:
            season_number = 0
            season_name = 'Season 0'
        elif None is season_number and None is not season_name:
            season_match = re.search(r"(\d+)", season_name)
            if season_match:
                season_number = int(season_match.group(1))
            else:
                season_number = 0
        else:
            season_name = f"Season {season_number}"

        return self.create_or_get_season(series_name, season_name, season_number)

