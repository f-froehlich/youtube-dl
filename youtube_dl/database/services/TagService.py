from youtube_dl.database.DatabaseService import DatabaseService
from youtube_dl.database.models.Tag import Tag


class TagService(DatabaseService):

    def create_or_get_tag(self, tag_name):

        tag_query = self._session.query(Tag) \
            .filter(Tag.name == tag_name)

        tag = tag_query.one_or_none()

        if tag is None:
            tag = Tag(name=tag_name)
            self._session.add(tag)

        return tag

    def create_or_get_tags_from_info_dict(self, info_dict):
        tags = info_dict.get('tags', None)

        if None is tags:
            return []

        return [self.create_or_get_tag(tag_name, ) for tag_name in tags]
