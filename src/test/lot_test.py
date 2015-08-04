import requests_mock

from src.pylex import LexApi

_api = LexApi(auth=('caspervg', 'lolcode'))
_base = 'http://sc4devotion.com/csxlex/api/v4'

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

