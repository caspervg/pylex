import os
import requests

from src.pylex.route import Route


class LotRoute(Route):

    def lot(self, id):
        return self._get_json('lot/{}', id)

    def all(self):
        return self._get_json('lot/all')

    def download(self, id, file_path):

        url = (self._base + 'lot/{}/download').format(id)
        r = requests.get(url, auth=self._auth, stream=True)
        file_name = r.headers['Content-Disposition'].split('"')[-2]

        if len(file_path) < 1:
            return

        with open(os.path.join(file_path, file_name), 'wb') as file:
            for chunk in r.iter_content(chunk_size=1024):
                if chunk:
                    file.write(chunk)
                    file.flush()
