from base64 import b64encode
import os
import requests

from .route import Route


class LotRoute(Route):
    """
    Contains endpoints related to LEX lots
    """

    def lot(self, id, user=True, dependencies=True, comments=True, votes=True, no_strip=False):
        """
        Retrieve the lot with given identifier

        :param id: Identifier of the lot to retrieve
        :param user: Should user (authenticated) information be returned (e.g. last_downloaded)
        :param dependencies: Should a dependency list be returned
        :param comments: Should a list of comments be returned
        :param votes: Should a list of votes be returned
        :param no_strip: Should XML/HTML tags be stripped in the returned lot description
        :return: Requested lot
        :rtype: dict
        """
        args = {}
        if user:
            args['user'] = 'true'
        if dependencies:
            args['dependencies'] = 'true'
        if comments:
            args['comments'] = 'true'
        if votes:
            args['votes'] = 'true'
        if no_strip:
            args['nostrip'] = 'true'

        return self._get_json('lot/{0}', id, **args)

    def all(self):
        """
        Retrieve a concise list of all available lots

        :return: List of all lots
        :rtype: list
        """
        return self._get_json('lot/all')

    def download(self, id, directory):
        """
        Download the file with given identifier to the given directory
        :param id: Identifier of the lot to download
        :param directory: Directory where the downloaded ZIP should be stored
        :return: None
        """
        url = (self._base + 'lot/{0}/download').format(id)
        r = requests.get(url, auth=self._auth, stream=True)
        file_name = r.headers['Content-Disposition'].split('"')[-2]

        if len(directory) < 1:
            return

        with open(os.path.join(directory, file_name), 'wb') as file:
            for chunk in r.iter_content(chunk_size=1024):
                if chunk:
                    file.write(chunk)
                    file.flush()

    def add(self, id):
        """
        Add the lot with given identifier to the user's download (later) list
        :param id: Identifier of the lot to add to the list
        :return: None
        """
        self._get('lot/{0}/download-list', id)

    def rate(self, id, comment=None, vote=None):
        """
        Add a rating (vote and/or comment) to the lot with given identifier
        :param id: Identifier to add the rating to
        :param comment: String with the comment to add. It should have len > 0 when entered.
        :param vote: int with the vote to add. It should be greater than 0 and smaller than 4 when entered.
        :return: Which elements were uploaded (list of 'rating' and/or 'comment')
        :rtype: list
        """

        rating = {}

        if vote is not None:
            if 1 <= vote <= 3:
                rating['rating'] = vote
        if comment is not None:
            if len(comment) > 0:
                rating['comment'] = comment

        url = self._base + 'lot/{0}/comment'.format(id)
        r = requests.post(url, auth=self._auth, params=rating)
        r.raise_for_status()
        return r.json()

    def set_dependencies(self, id, internal=list(), external=list()):
        """
        Sets the dependency string (for the LEX Dependency Tracker) for a lot.
        Requires administrator access.
        :param id: Identifier of the lot
        :param internal: List of dependency identifiers for internal files (LEX lots) that the lot depends on
        :param external: List of (name, link) tuples for external files (STEX, TSC, ...) that the lot depends on
        :return: Created dependency string that was sent to the server, in plaintext and base64 encoded
        :rtype: str
        """
        dependency_str = 'NO'
        if len(internal) > 0 or len(external) > 0:
            deps = internal
            for (name, link) in external:
                deps.append("{0}@{1}".format(name, link))
            dependency_str = '$'.join(str(x) for x in deps)

        params = {
            'string': b64encode(dependency_str.encode('ascii'))
        }

        url = self._base + 'lot/{0}/dependency-string'.format(id)
        r = requests.put(url, auth=self._auth, params=params)
        r.raise_for_status()

        return {
            'plain': dependency_str,
            'encoded': params['string']
        }
