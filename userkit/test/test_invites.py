from base_test import BaseTestCase
from util import rand_email, rand_str


class TestInvites(BaseTestCase):

    def test_create_invite(self):
        email = rand_email()
        invite = self.uk.invites.create_invite(to_email=email)
        self.assertEqual(invite.to_email, email.lower())
        self.assertTrue(hasattr(invite, 'token_raw'))

    def test_send_invite(self):
        email = rand_email()
        invite = self.uk.invites.send_invite(to_email=email)
        self.assertEqual(invite.to_email, email.lower())

    def test_get_invite(self):
        email = rand_email()
        created_invite = self.uk.invites.send_invite(to_email=email)
        fetched_invite = self.uk.invites.get_invite(created_invite.id)
        self.assertEqual(fetched_invite.id, created_invite.id)
        self.assertEqual(fetched_invite.to_email, created_invite.to_email)

    def test_get_invite_does_not_exist(self):
        inv = self.uk.invites.get_invite('wrong-id')
        self.assertIsNone(inv)

    def test_list_invites(self):
        invite_list = self.uk.invites.get_invites()
        self.assertTrue(hasattr(invite_list, 'next_page'))
        self.assertTrue(hasattr(invite_list[0], 'to_email'))

    def test_accept_invite(self):
        email = rand_email()
        invite = self.uk.invites.create_invite(to_email=email)
        user = self.uk.users.create_user(email=rand_email(),
                                         password=rand_str(14))

        invite = self.uk.invites.accept_invite(user.id, invite.token_raw)
        self.assertTrue(invite.accepted)

    # Util methods

    def test_invite__str__method(self):
        invite = self.uk.invites.send_invite(to_email=rand_email())
        try:
            s = invite.__str__()
        except Exception as e:
            self.fail('user.__str__() raises exception: %r' % e)
