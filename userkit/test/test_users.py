from base_test import BaseTestCase, BaseMockTestCase
from helper import DUMMY_USER, DUMMY_VERIFIED_PHONE_SUCCESS
from helper import DUMMY_VERIFIED_EMAIL_SUCCESS
from util import rand_str, rand_email
from userkit import error


class TestUsers(BaseTestCase):

    def test_create_user(self):
        email = rand_email()
        user = self.uk.users.create_user(email=email, password=rand_str(14))
        self.assertEqual(user.email, email.lower())

    def test_get_user(self):
        u = self.uk.users.create_user(email=rand_email(),
                                      password=rand_str(14))
        user = self.uk.users.get_user(u.id)
        self.assertEqual(user.id, u.id)

    def test_get_user_does_not_exist(self):
        u = self.uk.users.get_user('wrong-id')
        self.assertIsNone(u)

    def test_list_users(self):
        l = self.uk.users.get_users()
        self.assertIsInstance(l, list)
        self.assertTrue(hasattr(l, 'next_page'))
        self.assertTrue(hasattr(l[0], 'username'))

    def test_update_user(self):
        u = self.uk.users.create_user(email=rand_email(),
                                      password=rand_str(14), name="Name")
        new_name = "Test Name {}".format(rand_str())
        user = self.uk.users.update_user(u.id, name=new_name)
        self.assertEqual(user.name, new_name)

    def test_save_user(self):
        u = self.uk.users.create_user(email=rand_email(),
                                      password=rand_str(14), name="Name")
        new_name = "Test Name {}".format(rand_str())

        user = self.uk.users.get_user(u.id)
        user.name = new_name
        user.save()
        self.assertEqual(user.name, new_name)

    def test_disable_user(self):
        u = self.uk.users.create_user(email=rand_email(),
                                      password=rand_str(14))
        # Test the disable_user() function
        disabled = True
        user = self.uk.users.disable_user(u.id, disabled)
        self.assertEqual(user.disabled, disabled)

        # Return to original value (and test the user.disable() method)
        disabled = False
        user.disable(disabled)
        self.assertEqual(user.disabled, disabled)

    def test_login_and_logout_user(self):
        email, password = rand_email(), rand_str(14)
        u = self.uk.users.create_user(email=email, password=password)
        # Test login
        session = self.uk.users.login_user(email, password)
        self.assertTrue(hasattr(session, 'token'))

        # Test logout
        try:
            self.uk.users.logout_user(session.token)
        except Exception as e:
            self.fail(e)

    def test_get_user_by_session(self):
        email, password = rand_email(), rand_str(14)
        u = self.uk.users.create_user(email=email, password=password)

        session = self.uk.users.login_user(email, password)
        user = self.uk.users.get_user_by_session(session.token)
        self.assertEqual(user.id, u.id)

    def test_get_user_by_session_bad_token(self):
        self.assertRaises(error.UserAuthenticationError,
                          self.uk.users.get_user_by_session, 'very-bad-token')

    def test_get_current_user(self):
        email, password = rand_email(), rand_str(14)
        u = self.uk.users.create_user(email=email, password=password)
        session = self.uk.users.login_user(email, password)

        user = self.uk.users.get_current_user(session.token)
        self.assertEqual(user.id, u.id)

    def test_get_current_user_bad_token(self):
        # Bad session token should return None
        user = self.uk.users.get_current_user('very-bad-session')
        self.assertIsNone(user)

    def test_request_password_reset(self):
        u = self.uk.users.create_user(email=rand_email(),
                                      password=rand_str(14))
        try:
            self.uk.users.request_password_reset(u.email)
        except Exception as e:
            self.fail(e)

    def test_refresh_session(self):
        email, password = rand_email(), rand_str(14)
        u = self.uk.users.create_user(email=email, password=password)
        session1 = self.uk.users.login_user(email, password)
        session2 = self.uk.users.refresh_session(session1.token)
        self.assertTrue(hasattr(session2, 'token'))
        self.assertTrue(hasattr(session2, 'expires_in_secs'))


class TestUsersMock(BaseMockTestCase):
    """Tests which can't be run agains the live API server.

    For example: resetting a password when we don't have the reset
    token.
    """

    def test_pwreset_new_password(self):
        try:
            self.uk.users.reset_password('fake-pw-reset-token',
                                         'fake-new-pass')
        except Exception as e:
            self.fail(e)

    def test_set_user_auth_type(self):
        # Test new auth type
        try:
            self.uk.users.set_user_auth_type(DUMMY_USER['id'], 'password')
        except Exception as e:
            self.fail(e)

    # Verification tests ----------------------------------------------

    def test_send_phone_verification_code(self):
        try:
            self.uk.users.request_phone_verification_code(
                '+15555555555', 'sms')
        except Exception as e:
            self.fail(e)

    def test_send_email_verification_code(self):
        try:
            self.uk.users.request_email_verification_code(
                'fake@example.com')
        except Exception as e:
            self.fail(e)

    def test_verify_phone(self):
        success_token = self.uk.users.verify_phone('+15555555555', 'fake-code')
        self.assertEqual(success_token,
                         DUMMY_VERIFIED_PHONE_SUCCESS['verified_phone_token'])

    def test_verify_email(self):
        success_token = self.uk.users.verify_email('fake@example.com',
                                                   'fake-code')
        self.assertEqual(success_token,
                         DUMMY_VERIFIED_EMAIL_SUCCESS['verified_email_token'])

    def test_verify_phone_for_user(self):
        try:
            self.uk.users.verify_phone_for_user(DUMMY_USER['id'],
                                                '+15555555555', 'fake-code')
        except Exception as e:
            self.fail(e)

    def test_email_phone_for_user(self):
        try:
            self.uk.users.verify_email_for_user(
                DUMMY_USER['id'], 'fake@example.com', 'fake-code')
        except Exception as e:
            self.fail(e)

    # Utility tests ---------------------------------------------------

    def test_user__str__method(self):
        user = self.uk.users.get_user(DUMMY_USER['id'])
        try:
            s = user.__str__()
        except Exception as e:
            self.fail('user.__str__() raises exception: %r' % e)

    def test_session__str__method(self):
        session = self.uk.users.login_user('fake-uname', 'fake-pw')
        try:
            s = session.__str__()
        except Exception as e:
            self.fail('user.__str__() raises exception: %r' % e)
