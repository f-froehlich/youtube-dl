from youtube_dl.database.DatabaseService import DatabaseService
from youtube_dl.database.models.Category import Category


class CategoryService(DatabaseService):

    def create_or_get_category(self, category_name):

        category_query = self._session.query(Category) \
            .filter(Category.name == category_name)

        category = category_query.one_or_none()

        if category is None:
            category = Category(name=category_name)
            self._session.add(category)

        return category

    def create_or_get_categories_from_info_dict(self, info_dict):
        categories = info_dict.get('categories', None)

        if None is categories:
            return []

        return [self.create_or_get_category(category_name, ) for category_name in categories]
