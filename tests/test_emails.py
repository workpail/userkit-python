from .base_test import BaseTestCase


class TestEmails(BaseTestCase):
    """We can only test bad email_keys since a real key can only
    be obtained by UserKit POSTing to a developer's email_webhook
    endpoint.
    """

    def test_get_pending_email_bad_key(self):
        email = self.uk.emails.get_pending_email('completelywrong-key-here')
        self.assertIsNone(email)
