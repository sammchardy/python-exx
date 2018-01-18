# coding=utf-8

from exx.client import Client
from exx.exceptions import ExxAPIException, ExxRequestException
import pytest
import requests_mock


client = Client('api_key', 'api_secret')


def test_invalid_json():
    """Test Invalid response Exception"""

    with pytest.raises(ExxRequestException):
        with requests_mock.mock() as m:
            m.get('https://api.exx.com/data/v1/markets', text='<head></html>')
            client.get_markets()


def test_api_exception():
    """Test API response Exception"""

    with pytest.raises(ExxAPIException):
        with requests_mock.mock() as m:
            json_obj = {'error': '币种错误'}
            m.get('https://api.exx.com/data/v1/tickers', json=json_obj, status_code=200)
            client.get_tickers()


