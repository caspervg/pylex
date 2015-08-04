import os
import requests

from .route import Route


class LotRoute(Route):
    """
    Contains endpoints related to LEX lots
    """

    def lot(self, id, user=True, dependencies=True, comments=True, votes=True):
        """
        Retrieve the lot with given identifier

        :param id: Identifier of the lot to retrieve
        :param user: Should user (authenticated) information be returned (e.g. last_downloaded)
        :param dependencies: Should a dependency list be returned
        :param comments: Should a list of comments be returned
        :param votes: Should a list of votes be returned
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

        return self._get_json('lot/{}', id, **args)

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
        url = (self._base + 'lot/{}/download').format(id)
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
        self._get('lot/{}/download-list', id)

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

        url = self._base + 'lot/{}/comment'.format(id)
        r = requests.post(url, auth=self._auth, params=rating)
        r.raise_for_status()
        return r.json()
