import unittest
import userkit
import helper


class BaseTestCase(unittest.TestCase):

    def setUp(self):
        self.uk = userkit.UserKit('fake-a:pi-key',
                                  _requestor=helper.MockRequestor())