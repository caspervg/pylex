from nose.tools import eq_
import requests_mock

from src.pylex import LexApi

_api = LexApi(auth=('test_account', 'test_pass'))
_base = 'http://sc4devotion.com/csxlex/api/v4'


def test_categories():
    with requests_mock.Mocker() as mock:
        mock.register_uri('GET', _base + '/category/all', text="""{ "broad_category":[ { "id":1, "name":"Agriculture",
         "image":"250_MX_Agric.gif" }, { "id":2, "name":"Civic", "image":"250_MX_Civic.gif" },
          { "id":15, "name":"WFK - Canals", "image":"250_MXC_WFK-Canals.gif" } ], "lex_category":[ { "id":66,
          "name":"00 Locked" }, { "id":65, "name":"00 Outdated" }, { "id":35, "name":"Utilities - Power" },
          { "id":34, "name":"Utilities - Water" } ], "lex_type":[ { "id":5, "name":"BTE",
          "description":"Use for lots that depend or contribute to BSC Tracking Enabled Rewards." },
          { "id":19, "name":"CAM files", "description":"All basic CAM files" }, { "id":2, "name":"W2W",
          "description":"All Wall to Wall types of buildings" }, { "id":7, "name":"Water",
          "description":"Water Mods" } ], "group":[ { "id":4, "name":"BSC - VIP girafe flora", "author":"girafe" },
          { "id":2, "name":"CAL Canals", "author":"callagrafx" }, { "id":6, "name":"Sea- and Retaining Walls",
          "author":"ADMIN" }, { "id":5, "name":"Ships", "author":"ADMIN" } ], "author":[ { "id":1, "name":"ADMIN" },
          { "id":6509, "name":"andisart" }, { "id":15381, "name":"z" }, { "id":5275, "name":"zero7" } ] }""")

        cats = _api.category_route().all()

        eq_(len(cats['broad_category']), 3)
        eq_(cats['broad_category'][0]['image'], '250_MX_Agric.gif')
        eq_(cats['lex_category'][0]['id'], 66)
        eq_(cats['lex_type'][0]['description'],
            'Use for lots that depend or contribute to BSC Tracking Enabled Rewards.')
        eq_(cats['group'][0]['author'], 'girafe')
        eq_(cats['author'][0]['name'], 'ADMIN')


def test_broad():
    with requests_mock.Mocker() as mock:
        mock.register_uri('GET', _base + '/category/broad-category', text="""[ { "id":1, "name":"Agriculture",
         "image":"250_MX_Agric.gif" }, { "id":2, "name":"Civic", "image":"250_MX_Civic.gif" },
          { "id":15, "name":"WFK - Canals", "image":"250_MXC_WFK-Canals.gif" } ]""")

        cats = _api.category_route().broad_categories()
        eq_(len(cats), 3)
        eq_(cats[0]['image'], '250_MX_Agric.gif')


def test_lex_types():
    with requests_mock.Mocker() as mock:
        mock.register_uri('GET', _base + '/category/lex-type', text="""[ { "id":5, "name":"BTE",
          "description":"Use for lots that depend or contribute to BSC Tracking Enabled Rewards." },
          { "id":19, "name":"CAM files", "description":"All basic CAM files" }, { "id":2, "name":"W2W",
          "description":"All Wall to Wall types of buildings" }, { "id":7, "name":"Water",
          "description":"Water Mods" } ]""")

        cats = _api.category_route().lex_types()
        eq_(len(cats), 4)
        eq_(cats[-1]['id'], 7)


def test_lex_categories():
    with requests_mock.Mocker() as mock:
        mock.register_uri('GET', _base + '/category/lex-category', text="""[ { "id":66,
          "name":"00 Locked" }, { "id":65, "name":"00 Outdated" }, { "id":35, "name":"Utilities - Power" },
          { "id":34, "name":"Utilities - Water" } ]""")

        cats = _api.category_route().lex_categories()
        eq_(len(cats), 4)
        eq_(cats[1]['name'], '00 Outdated')


def test_groups():
    with requests_mock.Mocker() as mock:
        mock.register_uri('GET', _base + '/category/group', text="""[ { "id":4, "name":"BSC - VIP girafe flora",
         "author":"girafe" },{ "id":2, "name":"CAL Canals", "author":"callagrafx" },
         { "id":6, "name":"Sea- and Retaining Walls", "author":"ADMIN" },
         { "id":5, "name":"Ships", "author":"ADMIN" } ]""")

        cats = _api.category_route().groups()
        eq_(len(cats), 4)
        eq_(cats[0]['name'], 'BSC - VIP girafe flora')


def test_authors():
    with requests_mock.Mocker() as mock:
        mock.register_uri('GET', _base + '/category/group', text="""[ { "id":4, "name":"BSC - VIP girafe flora",
         "author":"girafe" },{ "id":2, "name":"CAL Canals", "author":"callagrafx" },
         { "id":6, "name":"Sea- and Retaining Walls", "author":"ADMIN" },
         { "id":5, "name":"Ships", "author":"ADMIN" } ]""")

        cats = _api.category_route().groups()
        eq_(len(cats), 4)
        eq_(cats[0]['name'], 'BSC - VIP girafe flora')
