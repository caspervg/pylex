from .route import Route


class SearchRoute(Route):

    def search(self, start=0, amount=15, order='asc', concise=False, user=True, dependencies=True, comments=True,
               votes=True, filters=None):
        """
        Search the LEX
        :param start: Start at this result number
        :param amount: Number of results to return
        :param order: Ordering of the results ('asc' or 'desc')
        :param concise: Return only concise results (name and id)
        :param user: Should user (authenticated) information be returned (e.g. last_downloaded)
        :param dependencies: Should a dependency list be returned
        :param comments: Should a list of comments be returned
        :param votes: Should a list of votes be returned
        :param filters: Extra filters to add to the search. At least one is required. See `the LEX API documentation
        <https://github.com/caspervg/SC4Devotion-LEX-API/blob/master/documentation/Search.md#filtering-parameters>` for
        more information about the possibilities. Use a dictionary with the name of the filter as key, and the filter
        value as value.
        :return: List of search results. Can be empty, if no results match the requested filters.
        :rtype: list
        """
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
