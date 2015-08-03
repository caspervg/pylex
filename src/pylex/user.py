import requests
from src.pylex.route import Route


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
