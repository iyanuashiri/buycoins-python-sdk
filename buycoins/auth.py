# Buycoin Python SDK
# Copyright 2021 Iyanuoluwa Ajao
# See LICENCE for details.

"""
Authentication is handled by the :any:`Airtable` class.

>>> airtable = Airtable(base_key, table_name, api_key)
Note:
    You can also use this class to handle authentication for you if you
    are making your own wrapper:
    >>> auth = BuycoinsAuth(api_key)
    >>>
    >>> response = requests.get('https://api.airtable.com/v0/{basekey}/{table_name}', auth=auth)
"""

from requests.auth import AuthBase


class BuycoinsAuth(AuthBase):
    def __int__(self, api_key):
        """
        Authentication used by Buycoin
        :param api_key:
        :return:
        """
        self.api_key = api_key

    def __call__(self, request):
        auth_token = {"Authorization": f"Basic {self.api_key}"}
        request.headers.update(auth_token)
        return request

