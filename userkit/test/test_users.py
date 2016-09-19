import unittest
import userkit
import helper
from helper import DUMMY_SESSION, DUMMY_USER, DUMMY_SUCCESS
from helper import DUMMY_USER_LIST


class TestUsers(unittest.TestCase):

    def setUp(self):
        self.uk = userkit.UserKit('fake-a:pi-key',
                                  _requestor=helper.MockRequestor())

    def test_get_user(self):
        user = self.uk.users.fetch_user_by_userid(DUMMY_USER['id'])
        self.assertEqual(user.email, DUMMY_USER['email'])

    def test_list_users(self):
        l = self.uk.users.fetch_all()
        self.assertIsInstance(l, list)
        self.assertTrue(hasattr(l, 'next_page'))
        self.assertTrue(hasattr(l[0], 'username'))

    def test_create_user(self):
        user = self.uk.users.create_user(email='fake@example.com')
        self.assertEqual(user.email, DUMMY_USER['email'])

    def test_update_user(self):
        new_name = "The New Name"
        user = self.uk.users.fetch_user_by_userid(DUMMY_USER['id'])
        user.name = new_name
        user.save()
        self.assertEqual(user.name, new_name)

    def test_login_user(self):
        session = self.uk.users.login_user('fake@example.com', 'pass1234')
        self.assertEqual(session.token, DUMMY_SESSION['token'])

    def test_logout_user(self):
        success = self.uk.users.logout_user('fake-token')
        self.assertTrue(success)

    def test_get_current_user(self):
        user = self.uk.users.get_current_user('fake-token')
        self.assertEqual(user.email, DUMMY_USER['email'])

    def test_request_password_reset(self):
        success = self.uk.users.request_password_reset(DUMMY_USER['email'])
        self.assertTrue(success)

    def test_pwreset_new_password(self):
        success = self.uk.users.reset_password('fake-pw-reset-token',
                                               'fake-new-pass')
        self.assertTrue(success)

    def test_disable_user(self):
        user = self.uk.users.fetch_user_by_userid(DUMMY_USER['id'])
        success = user.disable(True)
        self.assertTrue(success)
        self.assertEqual(user.disabled, True)

    def test_set_user_auth_type(self):
        success = self.uk.users.assign_user_auth_type(
            DUMMY_USER['id'], 'two_factor')
        self.assertTrue(success)
