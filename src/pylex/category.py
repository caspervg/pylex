from src.pylex.route import Route


class CategoryRoute(Route):
    def all(self):
        return self._get_json('category/all')

    def broad_categories(self):
        return self._get_json('category/broad-category')

    def lex_categories(self):
        return self._get_json('category/lex-category')

    def lex_types(self):
        return self._get_json('category/lex-type')

    def groups(self):
        return self._get_json('category/group')

    def authors(self):
        return self._get_json('category/author')