from youtube_dl.database.DatabaseService import DatabaseService
from youtube_dl.database.models.Extractor import Extractor


class ExtractorService(DatabaseService):

    def create_or_get_extractor(self, extractor_name, extractor_key):

        extractor_query = self._session.query(Extractor) \
            .filter(Extractor.name == extractor_name)

        extractor = extractor_query.one_or_none()

        if extractor is None:
            extractor = Extractor(name=extractor_name, extractor_key=extractor_key)
            self._session.add(extractor)

        return extractor

    def create_or_get_extractor_from_info_dict(self, info_dict):
        extractor_key = info_dict.get('extractor_key', None)
        extractor_name = info_dict.get('extractor', None)

        return self.create_or_get_extractor(extractor_name, extractor_key)
