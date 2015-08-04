from src.pylex.route import Route


class SearchRoute(Route):

    def search(self, start=0, amount=15, order='asc', concise=False, user=True, dependencies=True, comments=True,
               votes=True, filters=None):
        if not filters or len(filters.keys()) < 1:
            raise Exception('Need at least one filter in the "filters" dict')

        main = {
            'start': start,
            'amount': amount,
            'order': order,
        }

        if user:
            main['user'] = 'true'
        if dependencies:
            main['dependencies'] = 'true'
        if comments:
            main['comments'] = 'true'
        if votes:
            main['votes'] = 'true'
        if concise:
            main['concise'] = 'true'

        main.update(filters)
        return self._get_json('search', **main)
