# Buycoin Python SDK
# Copyright 2021 Iyanuoluwa Ajao
# See LICENCE for details.


class BuycoinsException(Exception):
    """ Class that handles HTTP exception"""

    def __init__(self, reason, response=None, api_code=None):
        """
        Constructor for the BuycoinException Class

        :param reason:
        :param response:
        :param api_code:
        """
        self.reason = reason
        self.response = response
        self.api_code = api_code
        super().__init__(reason)

    def __str__(self):
        return self.reason


class RateLimitException(BuycoinsException):

    def __init__(self, reason, period_remaining):
        pass
