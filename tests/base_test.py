import os
import unittest
import userkit
from . import helper


class BaseTestCase(unittest.TestCase):

    def setUp(self):
        api_key = os.environ.get('USERKIT_KEY')
        if not api_key:
            raise ValueError('Missing environmental variable USERKIT_KEY. '
                             'Run tests like this: '
                             '`USERKIT_KEY=<key> python -m unittest discover`')

        self.uk = userkit.UserKit(api_key)


class BaseMockTestCase(unittest.TestCase):

    uk = None

    @classmethod
    def setUpClass(cls):
        cls.uk = userkit.UserKit('fake-key', _requestor=helper.MockRequestor())
