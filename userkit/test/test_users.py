from base_test import BaseTestCase
from helper import DUMMY_SESSION, DUMMY_USER, DUMMY_VERIFIED_PHONE_SUCCESS
from helper import DUMMY_VERIFIED_EMAIL_SUCCESS


class TestUsers(BaseTestCase):

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

    # Utility methods

    def test_user__str__method(self):
        user = self.uk.users.fetch_user_by_userid(DUMMY_USER['id'])
        try:
            s = user.__str__()
        except Exception as e:
            self.fail('user.__str__() raises exception: %r' % e)


class TestVerification(BaseTestCase):

    def test_send_phone_verification_code(self):
        success = self.uk.users.request_phone_verification_code(
            '+15555555555', 'sms')
        self.assertTrue(success)

    def test_send_email_verification_code(self):
        success = self.uk.users.request_email_verification_code(
            'fake@example.com')
        self.assertTrue(success)

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
        success = self.uk.users.verify_phone_for_user(DUMMY_USER['id'],
                                                '+15555555555', 'fake-code')
        self.assertTrue(success)

    def test_email_phone_for_user(self):
        success = self.uk.users.verify_email_for_user(
            DUMMY_USER['id'], 'fake@example.com', 'fake-code')
        self.assertTrue(success)


class TestSession(BaseTestCase):

    def test_session__str__method(self):
        session = self.uk.users.login_user('fake-uname', 'fake-pw')
        try:
            s = session.__str__()
        except Exception as e:
            self.fail('user.__str__() raises exception: %r' % e)
