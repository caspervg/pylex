import json
from nose.tools import ok_, eq_
import requests_mock

from src.pylex import LexApi

_api = LexApi(auth=('caspervg', 'lolcode'))
_base = 'http://sc4devotion.com/csxlex/api/v4'

def test_lot():
    with requests_mock.Mocker() as mock:
        mock.register_uri('GET', _base + '/lot/10', text="""{
          "id": 10,
          "name": "Praiodan Central Subway Station BSC",
          "version": "1.0",
          "num_downloads": 5802,
          "author": "praiodan",
          "is_exclusive": false,
          "description": "You've been looking for a central subway station?",
          "images": {
            "primary": "http:\/\/mydomain.com\/file_exchange\/images\/centralsubway_s.jpg",
            "secondary": "http:\/\/mydomain.com\/file_exchange\/images\/centralsubway_sn.jpg"
          },
          "link": "http:\/\/mydomain.com\/file_exchange\/lex_filedesc.php?lotGET=10",
          "is_certified": true,
          "is_active": true,
          "upload_date": "2007-01-12T00:00:00+0000",
          "update_date": "2007-02-08T00:00:00+0000",
          "filesize": "0.00"
         }""")
        mock.register_uri('GET', _base + '/lot/10?comments=true&dependencies=true&votes=true', text="""{
          "id": 10,
          "name": "Praiodan Central Subway Station BSC",
          "version": "1.0",
          "num_downloads": 5802,
          "author": "praiodan",
          "is_exclusive": false,
          "description": "You've been looking for a central subway station?",
          "images": {
            "primary": "http:\/\/mydomain.com\/file_exchange\/images\/centralsubway_s.jpg",
            "secondary": "http:\/\/mydomain.com\/file_exchange\/images\/centralsubway_sn.jpg"
          },
          "link": "http:\/\/mydomain.com\/file_exchange\/lex_filedesc.php?lotGET=10",
          "is_certified": true,
          "is_active": true,
          "upload_date": "2007-01-12T00:00:00+0000",
          "update_date": "2007-02-08T00:00:00+0000",
          "filesize": "0.00",
          "comments": [
            {
              "id": 35371,
              "user": "nightshadow666",
              "text": "Sehr sch\u00f6ne Arbeit! Passt perfekt f\u00fcr mein Berlin Projekt!!!",
              "date": "2014-06-20T00:00:00+0000",
              "by_author": false,
              "by_admin": false
            },
            {
              "id": 27,
              "user": "blackbeard",
              "text": "Awesome thanx for sharing.",
              "date": "2007-01-12T00:00:00+0000",
              "by_author": false,
              "by_admin": false
            }
          ],
          "votes": {
            "1": 5,
            "2": 1,
            "3": 0
          },
          "dependencies": {
            "status": "ok",
            "count": 1,
            "list": [
              {
                "internal": true,
                "id": 443,
                "name": "BSC Essentials",
                "status": {
                  "ok": true,
                  "deleted": false,
                  "superseded": false,
                  "superseded_by": -1,
                  "locked": false
                }
              }
            ]
          }
        }""")

        lot = _api.lot_route().lot(10, user=False, dependencies=False, comments=False, votes=False)
        ok_("dependencies" not in lot)
        ok_("last_downloaded" not in lot)
        ok_("comments" not in lot)
        ok_("votes" not in lot)
        eq_(lot['id'], 10)

        lot = _api.lot_route().lot(10)
        ok_("dependencies" in lot)
        ok_("last_downloaded" not in lot)
        ok_("comments" in lot)
        ok_("votes" in lot)
        eq_(lot['id'], 10)


def test_all():
    with requests_mock.Mocker() as mock:
        mock.register_uri('GET', _base + '/lot/all', text="""[
           {
              "id":2,
              "name":"CSX Farm SF - Veronique"
           },
           {
              "id":3,
              "name":"BLS Farm Jacky's Coach House Farm"
           },
           {
              "id":5,
              "name":"BRT Coal Mine BSC"
           },
           {
              "id":6,
              "name":"CSX Civic - National Library"
           },
           {
              "id":7,
              "name":"MBEAR Palazzo Bufalini BSC"
           }
        ]""")

        lots = _api.lot_route().all()
        eq_(len(lots), 5)
        eq_(lots[0]['id'], 2)
        eq_(lots[-1]['name'], 'MBEAR Palazzo Bufalini BSC')


def test_download():
    with requests_mock.Mocker() as mock:
        mock.register_uri('GET', _base + '/lot/2/download', headers={
            'Content-Disposition': 'attachment; filename="file2.zip"'
        })
        mock.register_uri('GET', _base + '/lot/50/download', headers={
            'Content-Disposition': 'attachment; filename="file50.zip"'
        })
        _api.lot_route().download(2, '')    # normally the second argument should be a file path
        _api.lot_route().download(50, '')   # normally the second argument should be a file path


def add_test():
    with requests_mock.Mocker() as mock:
        mock.register_uri('GET', _base + '/lot/2/download-list')
        _api.lot_route().add(2)

def rate_test():
    with requests_mock.Mocker() as mock:
        mock.register_uri('POST', _base + '/lot/2/comment?comment=blah&rating=3', text="""["comment", "rating"]""")
        rate = _api.lot_route().rate(2, comment="blah", vote=3)
        eq_(len(rate), 2)
        eq_(rate[0], "comment")
        eq_(rate[1], "rating")

        mock.register_uri('POST', _base + '/lot/2/comment?comment=blah', text="""["comment"]""")

        rate = _api.lot_route().rate(2, comment="blah")
        eq_(len(rate), 1)
        eq_(rate[0], "comment")

        mock.register_uri('POST', _base + '/lot/2/comment?rating=2', text="""["rating"]""")

        rate = _api.lot_route().rate(2, vote=2)
        eq_(len(rate), 1)
        eq_(rate[0], "rating")

        mock.register_uri('POST', _base + '/lot/2/comment', text="""[]""")

        rate = _api.lot_route().rate(2)
        eq_(len(rate), 0)
