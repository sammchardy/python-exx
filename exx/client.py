# coding=utf-8

import hashlib
import hmac
import time
import requests

from operator import itemgetter

from .exceptions import ExxAPIException, ExxRequestException


class Client(object):

    API_URL = 'https://api.exx.com/data/v1'
    PRIVATE_URL = 'https://trade.exx.com/api'

    SIDE_BUY = 'buy'
    SIDE_SELL = 'sell'

    def __init__(self, api_key, api_secret):
        """Exx API Client constructor

        https://www.exx.com/help/restApi

        :param api_key: Api Token Id
        :type api_key: string
        :param api_secret: Api Secret
        :type api_secret: string

        .. code:: python

            client = Client(api_key, api_secret)

        """

        self.API_KEY = api_key
        self.API_SECRET = api_secret
        self.session = self._init_session()

    def _init_session(self):

        session = requests.session()
        headers = {'Accept': 'application/json'}
        session.headers.update(headers)
        return session

    def _ordered_query_string(self, data):
        """Convert params to ordered query string

        :param data:
        :return:

        """
        params = []
        for key, value in data.items():
            params.append((key, value))
        # sort parameters by key
        params.sort(key=itemgetter(0))
        return '&'.join(["{}={}".format(d[0], d[1]) for d in params])

    def _generate_signature(self, query_string):
        """Generate the call signature

        :param path:
        :param data:
        :param nonce:

        :return: signature string

        """

        m = hmac.new(self.API_SECRET.encode('utf-8'), query_string.encode('utf-8'), hashlib.sha512)
        return m.hexdigest()

    def _create_uri(self, path, private=False):
        url = self.API_URL
        if private:
            url = self.PRIVATE_URL
        return '{}/{}'.format(url, path)

    def _request(self, method, path, signed, **kwargs):

        kwargs['data'] = kwargs.get('data', {})

        uri = self._create_uri(path, signed)
        query_string = ''

        if signed:
            # generate signature
            kwargs['data']['nonce'] = int(time.time() * 1000)
            kwargs['data']['accesskey'] = self.API_KEY

        if len(kwargs['data'].keys()):
            query_string = self._ordered_query_string(kwargs['data'])

        if signed:
            query_string += '&signature={}'.format(self._generate_signature(query_string))

        del(kwargs['data'])

        uri += '?{}'.format(query_string)

        response = getattr(self.session, method)(uri, **kwargs)
        return self._handle_response(response)

    def _handle_response(self, response):
        """Internal helper for handling API responses from the Quoine server.
        Raises the appropriate exceptions when necessary; otherwise, returns the
        response.
        """

        if not str(response.status_code).startswith('2'):
            raise ExxAPIException(response)
        try:
            json = response.json()

            if 'error' in json:
                raise ExxAPIException(response)

            if 'code' in json and json['code'] != 100:
                raise ExxAPIException(response)

            return json
        except ValueError:
            raise ExxRequestException('Invalid Response: %s' % response.text)

    def _get(self, path, signed=False, **kwargs):
        return self._request('get', path, signed, **kwargs)

    # Market Endpoints

    def get_markets(self):
        """Get a list of markets

        .. code:: python

            markets = client.get_markets()

        :returns: dict of dicts

        .. code-block:: python

            {
                 "eos_btc":{
                     "amountScale":2,
                     "priceScale":6,
                     "maxLevels":0,
                     "isOpen":false
                 },
                 "etc_hsr":{
                     "amountScale":3,
                     "priceScale":3,
                     "maxLevels":0,
                     "isOpen":true
                 },
            }

        :raises:  ExxResponseException, ExxAPIException

        """

        return self._get('markets')

    # Ticker Endpoints

    def get_tickers(self):
        """Get all price tickers

        .. code:: python

            markets = client.get_markets()

        :returns: dict of dicts

        .. code-block:: python

            {
                "bts_btc":{
                    "vol":0.0,
                    "last":0,
                    "sell":0.0,
                    "buy":0.0,
                    "weekRiseRate":0.0,
                    "riseRate":0.0,
                    "high":0.0,
                    "low":0,
                    "monthRiseRate":0.0
                },
            }

        :raises:  ExxResponseException, ExxAPIException

        """

        return self._get('tickers')

    def get_ticker(self, symbol):
        """Get symbol price ticker

        :param symbol: required e.g eth_hsr
        :type symbol: str

        .. code:: python

            markets = client.get_ticker('eth_hsr')

        :returns: dict

        .. code-block:: python

            {
                "ticker": {
                    "vol": "1447.851",
                    "last": "30.487000000",
                    "sell": "30.499",
                    "buy": "30.487",
                    "weekRiseRate": -1.17,
                    "riseRate": 9.45,
                    "high": "30.812",
                    "low": "27.855",
                    "monthRiseRate": -0.99
                },
                "date": "1510383406453"
            }

        :raises:  ExxResponseException, ExxAPIException

        """

        data = {
            'currency': symbol
        }

        return self._get('ticker', False, data=data)

    # Order book endpoint

    def get_order_book(self, symbol):
        """Get the bid and asks for the symbol

        :param symbol: required e.g eth_hsr
        :type symbol: str

        .. code:: python

            markets = client.get_order_book('eth_hsr')

        :returns: dict

        .. code-block:: python

            {
                "asks": [
                    [
                        "32.831",   # price
                        "0.083"     # quantity
                    ]...
                ],
                "bids": [
                    [
                        "30.434",   # price
                        "10.766"    # quantity
                    ]...
                ],
                "timestamp" : Timestamp
            }

        :raises:  ExxResponseException, ExxAPIException

        """

        data = {
            'currency': symbol
        }

        return self._get('depth', False, data=data)

    def get_market_trades(self, symbol):
        """Get the trades for the symbol

        :param symbol: required e.g eth_hsr
        :type symbol: str

        .. code:: python

            trades = client.get_market_trades('eth_hsr')

        :returns: list of dicts

        .. code-block:: python

            [
                {
                    "amount"     : 0.933,
                    "price"      : 31.595,
                    "tid"        : 2583932,     # Trade ID
                    "type"       : "sell",      # Trade type
                    "date"       : 2583932,
                    "trade_type" : "ask",       # Order type
                }, ...
            ]

        :raises:  ExxResponseException, ExxAPIException

        """

        data = {
            'currency': symbol
        }

        return self._get('trades', False, data=data)

    # Order endpoints

    def create_order(self, symbol, order_type, price, amount):
        """Cancel an order

        :param symbol: e.g eth_hsr
        :type symbol: str
        :param order_type: type buy or sell
        :type symbol: str
        :param price: price to trade at
        :type symbol: str
        :param amount: amount to trade
        :type symbol: str

        .. code:: python

            order = client.create_order('eth_hsr', 'buy', '0.0012', '1023.2')

        :returns: dict

        .. code-block:: python

            {
                "code": 100,
                "message": "操作成功",
                "id": "13877"
            }

        :raises:  ExxResponseException, ExxAPIException

        """

        data = {
            'currency': symbol,
            'type': order_type,
            'price': price,
            'amount': amount
        }

        return self._get('order', True, data=data)

    def cancel_order(self, symbol, order_id):
        """Cancel an order

        :param symbol: required e.g eth_hsr
        :type symbol: str
        :param order_id: required e.g 123456789
        :type symbol: int

        .. code:: python

            res = client.cancel_order('eth_hsr', 123456789)

        :returns: dict

        .. code-block:: python

            {
                "code": "100",
                "message": "操作成功。"
            }

        :raises:  ExxResponseException, ExxAPIException

        """

        data = {
            'currency': symbol,
            'id': order_id
        }

        return self._get('cancel', True, data=data)

    def get_order(self, symbol, order_id):
        """Cancel an order

        :param symbol: required e.g eth_hsr
        :type symbol: str
        :param order_id: required e.g 123456789
        :type symbol: int

        .. code:: python

            order = client.get_order('eth_hsr', 123456789)

        :returns: dict

        .. code-block:: python

            {
                "fees": 0,
                "total_amount": 1,
                "trade_amount": 0,
                "price": 31,
                "currency": “eth_hsr",
                "id": "13877",
                "trade_money": 0,
                "type": "buy",
                "trade_date": 1509728383300,
                "status": 0
            }

        :raises:  ExxResponseException, ExxAPIException

        """

        data = {
            'currency': symbol,
            'id': order_id
        }

        return self._get('getOrder', True, data=data)

    def get_open_orders(self, symbol, order_type=None, page=1):
        """Get a list of open buy or sell orders, 10 at a time

        :param symbol: e.g eth_hsr
        :type symbol: str
        :param order_type: optional - type buy or sell
        :type symbol: str
        :param page: page index starting at 1
        :type page: int

        .. code:: python

            # get first page of open orders
            orders = client.get_open_orders('hsr_eth')

            # get first page of buy orders
            orders = client.get_open_orders('hsr_eth', 'buy')

            # second page of sell orders
            orders = client.get_open_orders('hsr_eth', 'sell', 2)

        :returns: list of dicts

        .. code-block:: python

            {
                "fees": 0,
                "total_amount": 1,
                "trade_amount": 0,
                "price": 31,
                "currency": “eth_hsr",
                "id": "13877",
                "trade_money": 0,
                "type": "buy",
                "trade_date": 1509728383300,
                "status": 0
            }

        :raises:  ExxResponseException, ExxAPIException

        """

        data = {
            'currency': symbol,
            'type': order_type,
            'pageIndex': page
        }
        if order_type:
            data['type'] = order_type

        return self._get('getOpenOrders', True, data=data)

    def get_balance(self):
        """Get your balance

        .. code:: python

            orders = client.get_balance()

        :returns: dict

        .. code-block:: python

            {
                "credits": [
                    {
                        "flatRatio": "0.1",
                        "userRatio": "0.0985",
                        "noticeRatio": "0.2",
                        "levels": 10,
                        "flatPrice": 11.01471399
                    }
                ],
                "funds": {
                    "BTS": {
                        "total": "10",
                        "freeze": "0",
                        "balance": "10",
                        "propTag": "BTS",
                        "credit_quota": "121.938066",
                        "credit_borrowed": "0",
                        "credit_interest": "0"
                    },
                    "MONA": {
                        "total": "0.966033",
                        "freeze": "0.966033",
                        "balance": "0",
                        "propTag": "MONA",
                        "credit_quota": "0",
                        "credit_borrowed": "0",
                        "credit_interest": "0"
                    },
                    ....
                    "ETH": {
                        "total": "10",
                        "freeze": "0",
                        "balance": "10",
                        "propTag": "ETH",
                        "credit_quota": "121.938066",
                        "credit_borrowed": "0",
                        "credit_interest": "0"
                    },
                    "LTC": {
                        "total": "0",
                        "freeze": "0",
                        "balance": "0",
                        "propTag": "LTC",
                        "credit_quota": "121.938066",
                        "credit_borrowed": "0",
                        "credit_interest": "0"
                    },
                    "QTUM": {
                        "total": "0.003",
                        "freeze": "0.003",
                        "balance": "0",
                        "propTag": "QTUM",
                        "credit_quota": "0",
                        "credit_borrowed": "9.65",
                        "credit_interest": "0.026252"
                    }
                }
            }

        :raises:  ExxResponseException, ExxAPIException

        """

        return self._get('getBalance', True)
