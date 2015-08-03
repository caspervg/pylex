from nose.tools import eq_
import requests_mock

from src.pylex import LexApi

_api = LexApi(auth=('test_account', 'test_pass'))
_base = 'http://sc4devotion.com/csxlex/api/v4'

def test_me():
    with requests_mock.Mocker() as mock:
        mock.register_uri('GET', _base + '/user', text="""{ "id":1, "fullname":"Test McTester",
        "username":"test_account", "registered":"2007-06-02T00:00:00+0000", "last_login":"2015-08-02T16:08:34+0000",
        "is_active":true, "user_level":1, "email":"example@domain.com", "login_count":949, "is_donator":true,
        "is_rater":true, "is_uploader":true, "is_author":false, "is_admin":false }""")
        me = _api.user_route().me()
        eq_(me['username'], 'test_account')


def test_user():
    with requests_mock.Mocker() as mock:
        mock.register_uri('GET', _base + '/user/1', text="""{ "id":1, "fullname":"Test McTester",
        "username":"test_account", "registered":"2007-06-02T00:00:00+0000", "last_login":"2015-08-02T16:08:34+0000",
        "is_active":true, "user_level":1, "email":"example@domain.com", "login_count":949, "is_donator":true,
        "is_rater":true, "is_uploader":true, "is_author":false, "is_admin":false }""")

        user = _api.user_route().user(1)
        eq_(user['username'], 'test_account')


def test_all_user():
    with requests_mock.Mocker() as mock:
        mock.register_uri('GET', _base + '/user/all', text="""[ { "id":11, "username":"account11" },
         { "id":12, "username":"account12" }, { "id":13, "username":"account13" } ]""")

        users = _api.user_route().all_user()
        eq_(users[0]['username'], 'account11')
        eq_(len(users), 3)

def test_dl_history():
    with requests_mock.Mocker() as mock:
        mock.register_uri('GET', _base + '/user/download-history', text="""[ { "record": { "id": 13147804,
        "last_downloaded": "2015-06-28T00:00:00-0500", "last_version": "2.0", "download_count": 8 },
        "lot": { "id": 3070, "name": "LEX Downloader X", "update_date": "2015-06-28T00:00:00-0500", "version": "2.0.1",
         "author": "caspervg" } }, { "record": { "id": 14234851, "last_downloaded": "2014-12-21T00:00:00-0600",
         "last_version": "1.2.0", "download_count": 1 }, "lot": { "id": 2876, "name": "DAMN Manager1.3.1",
         "update_date": "2015-07-22T00:00:00-0500", "version": "1.3.1", "author": "Yild" } },
         { "record": { "id": 12847184, "last_downloaded": "2015-07-30T00:00:00-0500", "last_version": "33 PR",
         "download_count": 5 }, "lot": { "id": 851, "name": "Network Addon Mod (Windows)",
         "update_date": "2015-07-29T00:00:00-0500", "version": "33 PR", "author": "NAM Team" } } ]""")

        his = _api.user_route().dl_history()
        eq_(len(his), 3)
        eq_(his[0]['lot']['name'], 'LEX Downloader X')


def test_dl_list():
    with requests_mock.Mocker() as mock:
        mock.register_uri('GET', _base + '/user/download-list', text="""[ { "record":{ "id":13099621 },
        "lot":{ "id":4, "name":"JRJ Props Vol4 Rural Walls", "update_date":null, "version":"1.0" } },
        { "record": { "id": 14776622 }, "lot": { "id": 3231, "name": "VIP vnaoned railway station",
        "update_date": "2015-07-31T00:00:00-0500", "version": "1.0", "author": "girafe"} } ]""")

        lis = _api.user_route().dl_list()
        eq_(len(lis), 2)
        eq_(lis[0]['record']['id'], 13099621)
        eq_(lis[0]['lot']['name'], 'JRJ Props Vol4 Rural Walls')

def test_register():
    with requests_mock.Mocker() as mock:
        mock.register_uri('POST', _base + '/user/register?username=user')

        _api.user_route().register('user', 'pass', 'me@example.com', 'Test User')

def test_activate():
    with requests_mock.Mocker() as mock:
        mock.register_uri('GET', _base + '/user/activate?activation_key=foobar')

        _api.user_route().activate('foobar')
