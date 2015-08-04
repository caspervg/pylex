from nose.tools import eq_, ok_
import requests_mock

from src.pylex import LexApi

_api = LexApi(auth=('test_account', 'test_pass'))
_base = 'http://sc4devotion.com/csxlex/api/v4'


def test_search():
    with requests_mock.Mocker() as mock:
        mock.register_uri('GET', _base + '/search?start=0&amount=15&order=asc&user=true&comments=true&dependencies=true'
                                         '&votes=true&creator=2&concise=true', text="""[
                                          { "id":2947, "name":"Diggis Streams Grass Base Set BSC" },
                                          { "id":2939, "name":"JENXFAUNA Crocodiles" } ]""")
        res = _api.search_route().search(
            concise=True,
            filters={
                'creator': 2
            }
        )
        eq_(len(res), 2)
        eq_(res[0]['id'], 2947)
        eq_(res[1]['name'], 'JENXFAUNA Crocodiles')

        mock.register_uri('GET', _base + '/search?start=0&amount=15&order=asc&user=true&comments=true&dependencies=true'
                                         '&votes=true&group=500', text="""[]""")

        res = _api.search_route().search(
            filters={
                'group': 500
            }
        )
        eq_(len(res), 0)
        ok_(type(res) == list)

        mock.register_uri('GET', _base + '/search?start=10&amount=5&order=desc&broad_category=250_MX_Transport.gif'
                                         '&query=BLS',
                          text="""  [
                                      {
                                        "id": 2423,
                                        "name": "BLS Farm - Porkies",
                                        "version": "1.0",
                                        "num_downloads": 1759,
                                        "author": "barbyw",
                                        "is_exclusive": false,
                                        "description": "The Real Porkies farm is owned by Frankie who was the goalie",
                                        "images": {
                                          "primary": "http:\/\/mydomain.com\/file_exchange\/images\/porkies_s.jpg",
                                          "secondary": "http:\/\/mydomain.com\/file_exchange\/images\/porkies_sn.jpg"
                                        },
                                        "link": "http:\/\/mydomain.com\/file_exchange\/lex_filedesc.php?lotGET=2423",
                                        "is_certified": true,
                                        "is_active": true,
                                        "upload_date": "2010-07-06T00:00:00+0000",
                                        "update_date": "2010-07-08T00:00:00+0000",
                                        "filesize": "0.00"
                                      },
                                      {
                                        "id": 2327,
                                        "name": "BLS Centre Georges Pompidou BSC",
                                        "version": "1.0",
                                        "num_downloads": 3403,
                                        "author": "barbyw",
                                        "is_exclusive": false,
                                        "description": "This strange looking inside out building is a museum in Paris",
                                        "images": {
                                          "primary": "http:\/\/mydomain.com\/file_exchange\/images\/centrepompidou_red.jpg",
                                          "secondary": "http:\/\/mydomain.com\/file_exchange\/images\/centrepompidou_ren.jpg"
                                        },
                                        "link": "http:\/\/mydomain.com\/file_exchange\/lex_filedesc.php?lotGET=2327",
                                        "is_certified": true,
                                        "is_active": true,
                                        "upload_date": "2010-01-11T00:00:00+0000",
                                        "update_date": null,
                                        "filesize": "0.00"
                                      }
                                    ]""")

        res = _api.search_route().search(start=10, amount=5, order='desc', filters={
            'broad_category': '250_MX_Transport.gif',
            'query': 'BLS'
        })

        eq_(len(res), 2)
        eq_(res[0]['id'], 2423)
        eq_(res[0]['name'], 'BLS Farm - Porkies')
        eq_(res[1]['version'], '1.0')
        eq_(res[1]['is_certified'], True)
