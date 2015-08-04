import requests


class Route(object):

    _base = 'http://sc4devotion.com/csxlex/api/v4/'
    _auth = (None, None)

    def with_auth(self, auth):
        self._auth = auth

    def _get_json(self, route, *args, **kwargs):
        return self._get(route, *args, **kwargs).json()

    def _get(self, route, *args, **kwargs):
        url = self._base + route.format(*args)
        r = requests.get(url, auth=self._auth, params=kwargs)
        r.raise_for_status()
        return r

