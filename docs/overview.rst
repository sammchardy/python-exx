Getting Started
===============

Installation
------------

``python-exx`` is available on `PYPI <https://pypi.python.org/pypi/python-exx/>`_.
Install with ``pip``:

.. code:: bash

    pip install python-exx

Register on EXX
---------------

Firstly `register an account with EXX <https://www.exx.com/r/e8d10713544a2da74f91178feae775f9>`_.

Generate an API Key
-------------------

To use signed account methods you are required to `create an API Key <https://www.exx.com/u/apil>`_ and save the key and secret.

Initialise the client
---------------------

Pass your API Key and Secret

.. code:: python

    from exx.client import Client
    client = Client(api_key, api_secret)

API Rate Limit
--------------

Each IP can send maximum of 1000 https requests per minute.
If you exceed 1000 requests, the system will automatically block the IP for one hour.
After an hour, the IP will be automatically unlocked.

Each user can send a maximum of 10 request within one second.

