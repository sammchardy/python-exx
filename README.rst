============================
Welcome to python-exx v0.0.2
============================

.. image:: https://img.shields.io/pypi/v/python-exx.svg
    :target: https://pypi.python.org/pypi/python-exx

.. image:: https://img.shields.io/pypi/l/python-exx.svg
    :target: https://pypi.python.org/pypi/python-exx

.. image:: https://img.shields.io/travis/sammchardy/python-exx.svg
    :target: https://travis-ci.org/sammchardy/python-exx

.. image:: https://img.shields.io/coveralls/sammchardy/python-exx.svg
    :target: https://coveralls.io/github/sammchardy/python-exx

.. image:: https://img.shields.io/pypi/wheel/python-exx.svg
    :target: https://pypi.python.org/pypi/python-exx

.. image:: https://img.shields.io/pypi/pyversions/python-exx.svg
    :target: https://pypi.python.org/pypi/python-exx

This is an unofficial Python wrapper for the `EXX exchange REST API v1 <https://www.exx.com/help/restApi>`_. I am in no way affiliated with EXX, use at your own risk.

If you came here looking for the `EXX exchange <https://www.exx.com/r/e8d10713544a2da74f91178feae775f9>`_ to purchase cryptocurrencies, then `go here <https://www.exx.com/r/e8d10713544a2da74f91178feae775f9>`_. If you want to automate interactions with EXX stick around.

Source code
  https://github.com/sammchardy/python-exx

Documentation
  https://python-exx.readthedocs.io/en/latest/

Make sure you update often and check the `Changelog <https://python-exx.readthedocs.io/en/latest/changelog.html>`_ for new features and bug fixes.

Features
--------

- Implementation of all Market Data and Account endpoints.
- Simple handling of authentication
- No need to generate timestamps yourself, the wrapper does it for you
- Response exception handling

Quick Start
-----------

`Register an account with Exx <https://www.exx.com/r/e8d10713544a2da74f91178feae775f9>`_.

`Generate an API Key <https://www.exx.com/u/api>`_ and save the key and secret.

.. code:: bash

    pip install python-exx


.. code:: python

    from exx.client import Client
    client = Client(api_key, api_secret)

    # get market details
    markets = client.get_markets()

    # get market depth
    depth = client.get_order_book('hsr_eth')

    # get all symbol prices
    prices = client.get_tickers()

    # get a symbol prices
    price = client.get_ticker('hsr_eth')

    # place an order
    order = client.create_order('eth_hsr', 'buy', '0.0012', '1023.2')

    # cancel an order
    res = client.cancel_order('eth_hsr', 1234567)

    # get order details
    order = client.get_order('eth_hsr', 1234567)

    # get open orders
    orders = client.get_open_orders('eth_hsr')

    # get open buy orders
    orders = client.get_open_orders('eth_hsr', 'buy')

    # get second page of open sell orders
    orders = client.get_open_orders('eth_hsr', 'sell', 2)


For more `check out the documentation <https://python-exx.readthedocs.io/en/latest/>`_.

Donate
------

If this library helped you out feel free to donate.

- ETH: 0xD7a7fDdCfA687073d7cC93E9E51829a727f9fE70
- LTC: LPC5vw9ajR1YndE1hYVeo3kJ9LdHjcRCUZ
- NEO: AVJB4ZgN7VgSUtArCt94y7ZYT6d5NDfpBo
- BTC: 1Dknp6L6oRZrHDECRedihPzx2sSfmvEBys

Other Exchanges
---------------

If you use `Binance <https://www.binance.com/?ref=10099792>`_ check out my `python-binance <https://github.com/sammchardy/python-binance>`_ library.

If you use `Quoinex <https://accounts.quoinex.com/sign-up?affiliate=PAxghztC67615>`_
or `Qryptos <https://accounts.qryptos.com/sign-up?affiliate=PAxghztC67615>`_ check out my `python-quoine <https://github.com/sammchardy/python-quoine>`_ library.

If you use `Kucoin <https://www.kucoin.com/#/?r=E42cWB>`_ check out my `python-kucoin <https://github.com/sammchardy/python-kucoin>`_ library.

If you use `IDEX <https://idex.market>`_ check out my `python-idex <https://github.com/sammchardy/python-idex>`_ library.

If you use `BigONE <https://big.one>`_ check out my `python-bigone <https://github.com/sammchardy/python-bigone>`_ library.

.. image:: https://analytics-pixel.appspot.com/UA-111417213-1/github/python-exx?pixel&useReferer
