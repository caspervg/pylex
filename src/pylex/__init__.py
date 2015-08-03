from src.pylex.category import CategoryRoute
from src.pylex.lot import LotRoute
from src.pylex.search import SearchRoute
from src.pylex.user import UserRoute

class LexApi(object):

    _auth = (None, None)
    _routes = {
        'lot': None,
        'user': None,
        'search': None,
        'category': None
    }

    def __init__(self,
                 auth=(None, None),
                 lot_route=LotRoute(),
                 user_route=UserRoute(),
                 search_route=SearchRoute(),
                 category_route=CategoryRoute()):
        self._routes['lot'] = lot_route
        self._routes['user'] = user_route
        self._routes['search'] = search_route
        self._routes['category'] = category_route
        self._auth = auth

    def lot_route(self):
        """
        Retrieves the lot routing
        :return: Lot routing
        :rtype: LotRoute
        """
        return self._get_route('lot')

    def user_route(self):
        """
        Retrieves the user routing
        :return: User routing
        :rtype: UserRoute
        """
        return self._get_route('user')

    def search_route(self):
        """
        Retrieves the search routing
        :return: Search routing
        :rtype: SearchRoute
        """
        return self._get_route('search')

    def category_route(self):
        """
        Retrieves the category routing
        :return: Category routing
        :rtype: CategoryRoute
        """
        return self._get_route('category')

    def _get_route(self, name):
        self._routes[name].with_auth(self._auth)
        return self._routes[name]
