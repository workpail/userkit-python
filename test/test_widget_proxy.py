import json
from base_test import BaseTestCase
from util import rand_str, rand_email


class TestUsers(BaseTestCase):

    def setUp(self):
        super(TestUsers, self).setUp()

        # Create a user for use with various tests
        user_data = {
            'email': rand_email(),
            'password': rand_str(14),
            'extras': {'score': 100},
        }
        body = widget_body('post', 'users', user_data)
        resp = self.uk.widget.proxy(body)
        self.user1 = resp.response_dict['data']['user']
        self.user1_password = user_data['password']
        self.user1_token = resp.response_dict['data']['session']['token']
        self.user1_token_private = resp.token_private

    def test_wprox_create_user(self):
        user_data = {
            'email': rand_email(),
            'password': rand_str(14),
            'extras': {'score': 100},
        }
        body = widget_body('post', 'users', user_data)
        resp = self.uk.widget.proxy(body)

        user = resp.response_dict['data']['user']
        # Should create and return the new user
        self.assertEqual(user['email'], user_data['email'].lower())
        self.assertEqual(user['extras']['score'], user_data['extras']['score'])

        # Should contain correct JSON string in resp.response
        response_str = json.dumps(resp.response_dict)
        self.assertEqual(resp.response, response_str)

    def test_wprox_login_user(self):
        # Good password should return session
        login_data = {
            'username': self.user1['email'],
            'password': self.user1_password,
        }
        body = widget_body('post', 'login', login_data)
        resp = self.uk.widget.proxy(body, self.user1_token_private)
        self.assertEqual(resp.response_dict['status_int'], 200)
        self.assertIn('token', resp.response_dict['data'])
        self.assertIsNotNone(resp.token_private)

        # Bad password should return an error
        login_data['password'] += 'bad'
        body = widget_body('post', 'login', login_data)
        resp = self.uk.widget.proxy(body, self.user1_token_private)
        self.assertEqual(resp.response_dict['status_int'], 400)
        self.assertIn('error', resp.response_dict['data'])


def widget_body(method, endpoint, payload, token=None, token_priv=None):
    body = {
        'method': method,
        'endpoint': endpoint,
        'payload': payload,
    }
    if token:
        body['data']['token'] = token

    if token_priv:
        body['token_private'] = token_priv

    return json.dumps(body)
