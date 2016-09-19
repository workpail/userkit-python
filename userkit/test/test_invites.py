from base_test import BaseTestCase
from helper import DUMMY_INVITE, DUMMY_INVITE_CREATE


class TestInvites(BaseTestCase):

    def test_create_invite(self):
        invite = self.uk.invites.create_invite(
            to_email=DUMMY_INVITE_CREATE['to_email'])
        self.assertEqual(invite.to_email, DUMMY_INVITE_CREATE['to_email'])
        self.assertTrue(hasattr(invite, 'token_raw'))

    def test_send_invite(self):
        invite = self.uk.invites.send_invite(
            to_email=DUMMY_INVITE['to_email'])
        self.assertEqual(invite.to_email, DUMMY_INVITE['to_email'])

    def test_get_invite(self):
        invite = self.uk.invites.fetch_invite(DUMMY_INVITE['id'])
        self.assertEqual(invite.id, DUMMY_INVITE['id'])

    def test_list_invites(self):
        invite_list = self.uk.invites.fetch_invites()
        self.assertTrue(hasattr(invite_list, 'next_page'))
        self.assertTrue(hasattr(invite_list[0], 'to_email'))

    def test_accept_invite(self):
        invite = self.uk.invites.accept_invite('fake-user-id', 'fake-token')
        self.assertTrue(invite.accepted)

    # Util methods

    def test_invite__str__method(self):
        invite = self.uk.invites.fetch_invite(DUMMY_INVITE['id'])
        try:
            s = invite.__str__()
        except Exception as e:
            self.fail('user.__str__() raises exception: %r' % e)
