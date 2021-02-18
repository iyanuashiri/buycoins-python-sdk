# Buycoin Python SDK
# Copyright 2021 Iyanuoluwa Ajao
# See LICENCE for details.

import base64
import logging

from ratelimit import limits, sleep_and_retry
from gql import Client
from gql.transport.requests import RequestsHTTPTransport

from buycoins.exceptions import BuycoinsException
from buycoins.mutations import (CREATE_ADDRESS, CREATE_DEPOSIT_ACCOUNT,
                                POST_LIMIT_ORDER, POST_MARKET_ORDER, BUY, SELL, SEND)
from buycoins.queries import (CURRENT_BUYCOINS_PRICE, GET_ORDERS, GET_MARKET_BOOK,
                              GET_PRICES, GET_ESTIMATED_NETWORK_FEE, GET_BALANCES)


base_url = 'https://backend.buycoins.tech/api'

MAX_CALLS = 300
ONE_MINUTE = 60

ORDER_SIDE = ['buy', 'sell']
CRYPTOCURRENCIES = ['bitcoin', 'ethereum', 'litecoin', 'naira_token', 'usd_coin', 'usd_tether']
STATUS = ['open', 'completed']

log = logging.getLogger(__name__)


class API:
    """Buycoin API"""

    def __init__(self, public_key, secret_key):
        """
        Constructor for the API Class
        """
        self.public_key = public_key
        self.secret_key = secret_key

    def _process_headers(self):
        credentials = (self.public_key + ':' + self.secret_key).encode('utf-8')
        base64_encoded_credentials = base64.b64encode(credentials).decode('utf-8')
        headers = {
            'Authorization': 'Basic ' + base64_encoded_credentials
        }
        return headers

    @sleep_and_retry
    @limits(calls=MAX_CALLS, period=ONE_MINUTE)
    def request(self, query, params=None):

        # Throw an error if auth is required and there is no authentication
        # if require_auth and not self.auth_handler:
        #     raise BuycoinsException('Missing Basic Auth public key or secret key')

        if params is None:
            params = {}

        # for key, value in kwargs.items():
        #     if value is None:
        #         continue
        #     if key in params:
        #         raise BuycoinsException(f'Multiple values for parameter {key} supplied!')
        #     params[key] = value

        transport = RequestsHTTPTransport(url=base_url, headers=self._process_headers())
        client = Client(transport=transport, fetch_schema_from_transport=True)
        result = client.execute(query, variable_values=params)

        return result

    def current_buycoin_price(self, side, mode='standard', cryptocurrency='bitcoin'):
        """
        Current Buycoin Price.

        :param side:
        :param mode: (``str``) Default is `standard`
        :param cryptocurrency: (``str``) The default is `bitcoin`. The cryptocurrency you want to trade.
        :return:

        Usage::
            >>> api.current_buycoin_price()
            >>> api.current_buycoin_price()

        Reference::

        """
        if side not in ORDER_SIDE:
            raise BuycoinsException(f"The 'side' parameter has a wrong value '{side}'.")

        if cryptocurrency not in CRYPTOCURRENCIES:
            raise BuycoinsException(f"The 'cryptocurrency' parameter has a wrong value '{cryptocurrency}'.")

        params = {'side': side, 'mode': mode, 'cryptocurrency': cryptocurrency}
        return self.request(query=CURRENT_BUYCOINS_PRICE, params=params)

    def get_orders(self, status=None):
        """
        Retrieve all your orders.

        :param status: (``str``, optional) The status of orders to fetch, either `open` or `completed`. You can fetch all orders too.
        :return:

        Usage::
            >>> api.get_orders()
            >>> api.get_orders('open')
            >>> api.get_orders('completed')

        Reference::
            https://developers.buycoins.africa/p2p/get-orders
        """
        if status is None:
            return self.request(query=GET_ORDERS)
        elif status not in STATUS:
            raise BuycoinsException(f"The 'status' parameter has a wrong value '{status}'.")

        params = {'status': status}
        return self.request(query=GET_ORDERS, params=params)

    def get_market_book(self, status=None):
        """
        Retrieve the market book.

        :param status: (``str``, optional) The status of orders to fetch, either `open` or `completed`. You can fetch all orders too.
        :return:

        Usage::
            >>> api.get_market_book()
            >>> api.get_market_book('open')
            >>> api.get_market_book('completed')

        Reference::
            https://developers.buycoins.africa/p2p/get-market-book
        """
        if status is None:
            return self.request(query=GET_MARKET_BOOK)
        elif status not in STATUS:
            raise BuycoinsException(f"The 'status' parameter has a wrong value '{status}'.")

        params = {'status': status}
        return self.request(query=GET_MARKET_BOOK, params=params)

    def get_prices(self, cryptocurrency=None):
        """
        Get all active prices or get a singular cryptocurrency prices.

        :param cryptocurrency: (``str``, optional). Type of cryptocurrency.
        :return:

        Usage::
            >>> api.get_prices()
            >>> api.get_prices('bitcoin')
            >>> api.get_prices('litecoin')

        """
        if cryptocurrency is None:
            return self.request(query=GET_PRICES)
        if cryptocurrency not in CRYPTOCURRENCIES:
            raise BuycoinsException(f"The 'cryptocurrency' parameter has a wrong value '{cryptocurrency}'.")

        params = {'cryptocurrency': cryptocurrency}
        return self.request(query=GET_PRICES, params=params)

    def get_estimated_network_fee(self, amount, cryptocurrency='bitcoin'):
        """
        Get estimated network fees before sending.

        :param amount: (``float``) Amount to send to an external address.
        :param cryptocurrency: (``str``) The default is `bitcoin`. Type of cryptocurrency.
        :return:

        Usage::
            >>> api.get_estimated_network_fee(0.01, 'bitcoin')

        Reference::
            https://developers.buycoins.africa/sending/network-fees
        """
        if not isinstance(amount, float):
            raise BuycoinsException(f"The 'amount' parameter has a wrong value '{amount}'.")

        if cryptocurrency not in CRYPTOCURRENCIES:
            raise BuycoinsException(f"The 'cryptocurrency' parameter has a wrong value '{cryptocurrency}'.")

        params = {'amount': amount, 'cryptocurrency': cryptocurrency}
        return self.request(query=GET_ESTIMATED_NETWORK_FEE, params=params)

    def get_balances(self, cryptocurrency=None):
        """
        Check Cryptocurrency account balances with the API.

        This will return all your balances or the balance of a particular cryptocurrency argument passed in.

        :param cryptocurrency: (``str``, optional). Type of cryptocurrency.
        :return:

        Usage::
            >>> api.get_balances()
            >>> api.get_balances('bitcoin')

        Reference::
            https://developers.buycoins.africa/sending/account-balances
        """
        if cryptocurrency is None:
            return self.request(query=GET_BALANCES)
        if cryptocurrency not in CRYPTOCURRENCIES:
            raise BuycoinsException(f"The 'cryptocurrency' parameter has a wrong value '{cryptocurrency}'.")

        params = {'cryptocurrency': cryptocurrency}
        return self.request(query=GET_BALANCES, params=params)

    def create_deposit_account(self, account_name):
        """
        Creating account to receive Naira.

        :param account_name: (``str``). Account name.
        :return:

        Usage::
            >>> api.create_deposit_account('tony stark')

        Reference::
            https://developers.buycoins.africa/naira-token-account/create-virtual-deposit-account
        """
        params = {'accountName': account_name}
        return self.request(query=CREATE_DEPOSIT_ACCOUNT, params=params)

    def post_limit_order(self, order_side, coin_amount, price_type, cryptocurrency='bitcoin', static_price=None,
                         dynamic_exchange_rate=None):
        """
        Place a limit order.

        :param order_side:
        :param coin_amount: (``float``). The amount of coin.
        :param price_type:
        :param cryptocurrency: (``str``) The default is `bitcoin`. Type of cryptocurrency.
        :param static_price: (````, optional)
        :param dynamic_exchange_rate: (````, optional)
        :return:

        Usage::
            >>> api.post_limit_order()

        Reference::
            https://developers.buycoins.africa/p2p/post-limit-order
        """

        if order_side not in ORDER_SIDE:
            raise BuycoinsException(f"The value for side parameter '{order_side}' is not correct")

        if cryptocurrency not in CRYPTOCURRENCIES:
            raise BuycoinsException(f"The 'cryptocurrency' parameter has a wrong value '{cryptocurrency}'.")

        # if price_type not in ['static', 'dynamic']:
        #     raise BuycoinsException(f'The value for side parameter {price_type} is not correct')

        if price_type is 'static' and static_price is None:
            raise BuycoinsException(f'When price_type is static, static_price is required.')

        if price_type is 'dynamic' and dynamic_exchange_rate is None:
            raise BuycoinsException(f'When price_type is dynamic, dynamic_exchange_rate is required.')

        params = {'coinAmount': coin_amount, 'orderSide': order_side, 'priceType': price_type,
                  'cryptocurrency': cryptocurrency, 'staticPrice': static_price,
                  'dynamic_exchange_rate': dynamic_exchange_rate}
        return self.request(query=POST_LIMIT_ORDER, params=params)

    def post_market_order(self, coin_amount, order_side, cryptocurrency='bitcoin'):
        """
        Place a market order.

        :param coin_amount: (``float``). The amount of coin.
        :param order_side: (``str``). The order side either buy or sell.
        :param cryptocurrency: (``str``) The default is `bitcoin`. Type of cryptocurrency.
        :return:

        Usage::
            >>> api.post_market_order()

        Reference::
            https://developers.buycoins.africa/p2p/post-market-order
        """
        if not isinstance(coin_amount, float):
            raise BuycoinsException(f"The 'amount' parameter has a wrong value '{coin_amount}'. ")

        if order_side not in ORDER_SIDE:
            raise BuycoinsException(f'The value for side parameter {order_side} is not correct')

        if cryptocurrency not in CRYPTOCURRENCIES:
            raise BuycoinsException(f"The 'cryptocurrency' parameter has a wrong value '{cryptocurrency}'.")

        params = {'coinAmount': coin_amount, 'orderSide': order_side, 'cryptocurrency': cryptocurrency}
        return self.request(query=POST_MARKET_ORDER, params=params)

    def buy(self, price, coin_amount, cryptocurrency='bitcoin'):
        """
        Buying cryptocurrency with the API.

        To place a buy order, you will need the ``id`` of an active price.

        Usage::
            >>> api.buy('QnV5Y29pbnNQcmljZS0zOGIwYTg1Yi1jNjA1LTRhZjAtOWQ1My01ODk1MGVkMjUyYmQ=', 0.002, cryptocurrency='bitcoin')

        :param price: The ``id`` of an active price.
        :param coin_amount: (``float``). Amount of coin to buy.
        :param cryptocurrency: (``str``) The default is `bitcoin`. Type of cryptocurrency.
        :return:

        :reference: https://developers.buycoins.africa/placing-orders/buy
        """
        if not isinstance(coin_amount, float):
            raise BuycoinsException(f"The 'amount' parameter has a wrong value '{coin_amount}'. ")

        if cryptocurrency not in CRYPTOCURRENCIES:
            raise BuycoinsException(f"The 'cryptocurrency' parameter has a wrong value '{cryptocurrency}'.")

        params = {'price': price, 'coin_amount': coin_amount, 'cryptocurrency': cryptocurrency}
        return self.request(query=BUY, params=params)

    def sell(self, price, coin_amount, cryptocurrency='bitcoin'):
        """
        Selling cryptocurrency with the API.

        :param price: (``str``). The ``id`` of an active price.
        :param coin_amount: (``float``). Amount of coin to sell.
        :param cryptocurrency: (``str``) The default is `bitcoin`. Type of cryptocurrency.
        :return:

        Usage::
            >>> response = api.get_prices('bitcoin')
            >>>
            >>> api.sell('QnV5Y29pbnNQcmljZS0zOGIwYTg1Yi1jNjA1LTRhZjAtOWQ1My01ODk1MGVkMjUyYmQ=', 0.01, 'bitcoin')

        Reference::
            https://developers.buycoins.africa/placing-orders/sell
        """
        if not isinstance(coin_amount, float):
            raise BuycoinsException(f"The 'amount' parameter has a wrong value '{coin_amount}'. ")

        if cryptocurrency not in CRYPTOCURRENCIES:
            raise BuycoinsException(f"The 'cryptocurrency' parameter has a wrong value '{cryptocurrency}'.")

        params = {'price': price, 'coin_amount': coin_amount, 'cryptocurrency': cryptocurrency}
        return self.request(query=SELL, params=params)

    def send(self, amount, address, cryptocurrency='bitcoin'):
        """
        Send Cryptocurrency with the API.

        :param amount: (``float``). Amount of coin to send.
        :param address: (``str``). On-chain address.
        :param cryptocurrency: (``str``) The default is `bitcoin`. Type of cryptocurrency.
        :return:

        Usage::
            >>> api.send(0.01, "1MmyYvSEYLCPm45Ps6vQin1heGBv3UpNbf", 'bitcoin')

        Reference::
            https://developers.buycoins.africa/sending/send

        """
        if not isinstance(amount, float):
            raise BuycoinsException(f"The 'amount' parameter has a wrong value '{amount}'. ")

        if cryptocurrency not in CRYPTOCURRENCIES:
            raise BuycoinsException(f"The 'cryptocurrency' parameter has a wrong value '{cryptocurrency}'.")

        params = {'amount': amount, 'address': address, 'cryptocurrency': cryptocurrency}
        return self.request(query=SEND, params=params)

    def create_address(self, cryptocurrency='bitcoin'):
        """
        create an address on BuyCoins to receive coins on the API.

        :param cryptocurrency: (``str``) The default is `bitcoin`. Type of cryptocurrency.
        :return:

        Usage::
            >>> api.create_address()
            >>> api.create_address('bitcoin')
            >>> api.create_address('litecoin')

        Reference::
            https://developers.buycoins.africa/receiving/create-address
        """

        if cryptocurrency not in CRYPTOCURRENCIES:
            raise BuycoinsException(f"The 'cryptocurrency' parameter has a wrong value '{cryptocurrency}'.")

        params = {'cryptocurrency': cryptocurrency}
        return self.request(query=CREATE_ADDRESS, params=params)

api = API('', '')
api.create_deposit_account('')
