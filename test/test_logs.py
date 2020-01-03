from .base_test import BaseTestCase
from .util import rand_str, rand_email
from userkit import error


class TestLogs(BaseTestCase):

    def test_custom_audit_log(self):
        # create a test user
        email = rand_email()
        user = self.uk.users.create_user(email=email, password=rand_str(14))
        # create a test audit log
        log = self.uk.logs.log_event(actor=user.id, actor_ip='::1', actor_useragent='TestLogs', actee=user.id,
                                     action='test.custom_audit_log', details='Testing custom audit logs')
        self.assertEqual(log.actor, user.id)
        self.assertEqual(log.actor_ip, '::1')
        self.assertEqual(log.actor_useragent, 'TestLogs')
        self.assertEqual(log.actee, user.id)
        self.assertEqual(log.action, 'test.custom_audit_log')
        self.assertEqual(log.details, 'Testing custom audit logs')

    def test_custom_audit_log_invalid_actor(self):
        # create a test user
        email = rand_email()
        user = self.uk.users.create_user(email=email, password=rand_str(14))
        self.assertRaises(error.InvalidRequestError, self.uk.logs.log_event,
                          actor='NOT_A_VAlID_USER_ID', actor_ip='::1', actor_useragent='TestLogs',
                          actee=user.id, action='test.custom_audit_log', details='Testing custom audit logs')

    def test_custom_audit_log_invalid_actee(self):
        # create a test user
        email = rand_email()
        user = self.uk.users.create_user(email=email, password=rand_str(14))
        self.assertRaises(error.InvalidRequestError, self.uk.logs.log_event,
                          actor=user.id, actor_ip='::1', actor_useragent='TestLogs',
                          actee='NOT_A_VAlID_USER_ID', action='test.custom_audit_log',
                          details='Testing custom audit logs')
