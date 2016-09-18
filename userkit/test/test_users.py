import unittest
import userkit
import helper


class TestUsers(unittest.TestCase):

    def setUp(self):
        self.uk = userkit.UserKit('fake-a:pi-key',
                                  _requestor=helper.MockRequestor())

    def test_get_user(self):
        user = self.uk.users.fetch_user_by_userid('fake-user-id')
        self.assertEqual(user.email, helper.DUMMY_USER['email'])

    def test_list_users(self):
        l = self.uk.users.fetch_all()
        self.assertIsInstance(l, list)
        self.assertTrue(hasattr(l, 'next_page'))
        self.assertTrue(hasattr(l[0], 'username'))

    def test_create_user(self):
        user = self.uk.users.create_user(email='fake@example.com')
        self.assertEqual(user.email, helper.DUMMY_USER['email'])

    def test_login_user(self):
        session = self.uk.users.login_user('fake@example.com', 'pass1234')
        self.assertEqual(session.token, helper.DUMMY_SESSION['token'])
