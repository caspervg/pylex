from .route import Route


class CategoryRoute(Route):
    def all(self):
        """
        Return all available categories
        :return: available categories
        :rtype: list
        """
        return self._get_json('category/all')

    def broad_categories(self):
        """
        Return all available broad categories
        :return: broad categories
        :rtype: list
        """
        return self._get_json('category/broad-category')

    def lex_categories(self):
        """
        Return all available LEX categories
        :return: LEX categories
        :rtype: list
        """
        return self._get_json('category/lex-category')

    def lex_types(self):
        """
        Return all available LEX types
        :return: LEX types
        :rtype: list
        """
        return self._get_json('category/lex-type')

    def groups(self):
        """
        Return all available groups
        :return: groups
        :rtype: list
        """
        return self._get_json('category/group')

    def authors(self):
        """
        Return all available authors (people with more than 1 file released on the LEX)
        :return: authors
        :rtype: list
        """
        return self._get_json('category/author')