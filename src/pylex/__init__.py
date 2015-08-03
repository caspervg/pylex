import requests

class Route(object):

    _base = 'http://sc4devotion.com/csxlex/api/v4/'
    _auth = (None, None)

    def with_auth(self, auth):
        self._auth = auth

    def _get_json(self, route, *args, **kwargs):
        url = self._base + route.format(*args)
        r = requests.get(url, auth=self._auth, params=kwargs)
        r.raise_for_status()
        return r.json()


class UserRoute(Route):

    def me(self):
        """
        Return the currently authenticated user
        :rtype: dict
        """
        return self._get_json('user')

    def user(self, id):
        """
        Return the user with given id
        :rtype: dict
        """
        return self._get_json('user/{}', id)

    def all_user(self, start=0, amount=10):
        """
        Return a list of all users
        :rtype: list
        """
        return self._get_json('user/all', start=start, amount=amount)

    def dl_history(self):
        """
        Return the download history of the authenticated user
        :rtype: dict
        """
        return self._get_json('user/download-history')

    def dl_list(self):
        """
        Return the download (later) list of the authenticated user
        :rtype: dict
        """
        return self._get_json('user/download-list')

    def register(self, username, password, email, full_name):
        """
        Registers a new user on the LEX
        :rtype: None
        """
        if all([username, password, email, full_name]):
            r = requests.post(self._base + 'user/register', params={
                'username': username,
                'password_1': password,
                'password_2': password,
                'email': email,
                'fullname': full_name
            })
            r.raise_for_status()
        else:
            raise Exception('None of the arguments may be "None"')

    def activate(self, key):
        """
        Activates a new registree on the LEX with given activation key
        :rtype: None
        """
        url = self._base + 'user/activate'
        r = requests.get(url, params={
            'activation_key': key
        })
        r.raise_for_status()


class LotRoute(Route):
    pass


class SearchRoute(Route):
    pass


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
