from youtube_dl.database.DatabaseService import DatabaseService
from youtube_dl.database.models.Series import Series


class SeriesService(DatabaseService):

    def create_or_get_series(self, series_name):
        series_query = self._session.query(Series).filter(Series.name == series_name)
        series = series_query.one_or_none()
        if None is series:
            series = Series(name=series_name)
            self._session.add(series)

        return series
