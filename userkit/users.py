from .user import User, USR_MUTABLE_FIELDS
from .session import Session
from . import error as error


class UserList(list):
    next_page = None


class UserManager:
    _rq = None

    def __init__(self, requestor):
        self._rq = requestor

    def get_current_user(self, token, token_private=None):
        if not token:
            return None
        try:
            return self.get_user_by_session(token, token_private)
        except error.UserAuthenticationError:
            return None

    def create_user(self, **kwargs):
        post_data = {}
        for field in USR_MUTABLE_FIELDS:
            if field in kwargs:
                post_data[field] = kwargs[field]

        uri = '/users'
        result_dict = self._rq.request('post', uri, post_data=post_data)
        user = User(self._rq, **result_dict)
        return user

    def update_user(self, user_id, **kwargs):
        post_data = {}
        for field in USR_MUTABLE_FIELDS:
            if field in kwargs:
                post_data[field] = kwargs[field]

        uri = '/users/{}'.format(user_id)
        result_dict = self._rq.request('post', uri, post_data=post_data)
        user = User(self._rq, **result_dict)
        return user

    def login_user(self, username, password, code=None):
        post_data = {'username': username, 'password': password}
        if code:
            post_data['code'] = code

        uri = '/users/login'
        result_dict = self._rq.request('post', uri, post_data=post_data)

        session = Session(**result_dict)
        return session

    def logout_user(self, token):
        uri = '/users/logout'
        self._rq.request('post', uri, headers={'X-User-Token': token})

    def get_user_by_session(self, token, token_private=None):
        uri = '/users/by_token'
        headers = {'X-User-Token': token}
        if token_private:
            headers['X-User-Token-Private'] = token_private

        result_dict = self._rq.request('get', uri,
                                       headers=headers)
        user = User(self._rq, **result_dict)
        return user

    def get_user(self, user_id):
        uri = '/users/%s' % user_id
        try:
            result_dict = self._rq.request('get', uri)
        except error.ResourceNotFoundError:
            return None
        return User(self._rq, **result_dict)

    def request_password_reset(self, username_or_email):
        uri = '/users/request_password_reset'
        self._rq.request('post', uri,
                         post_data={'username_or_email': username_or_email})

    def reset_password(self, pw_reset_token, new_password):
        uri = '/users/password_reset_new_password'
        self._rq.request('post', uri,
                         post_data={'token': pw_reset_token, 'password': new_password})

    def get_users(self, limit=25, next_page=None):
        uri_params = {}
        if limit:
            uri_params['limit'] = limit
        if next_page:
            uri_params['next_page'] = next_page

        uri = '/users'
        result_list = self._rq.request('get', uri, uri_params=uri_params)
        user_list = UserList()
        for user_dict in result_list.get('users', []):
            user = User(self._rq, **user_dict)
            user_list.append(user)

        user_list.next_page = result_list.get('next_page')
        return user_list

    def set_user_auth_type(self, user_id, auth_type, phone_number=None,
                           phone_token=None):
        post_data = {'auth_type': auth_type}
        if phone_number and phone_token:
            post_data['phone'] = phone_number
            post_data['phone_token'] = phone_token

        uri = '/users/%s/auth_type' % user_id
        self._rq.request('post', uri, post_data=post_data)

    def request_phone_verification_code(self, phone_number, send_method='sms'):
        uri = '/users/request_phone_verification_code'
        self._rq.request('post', uri,
                         post_data={'phone': phone_number, 'send_method': send_method})

    def verify_phone(self, phone_number, verification_code):
        uri = '/users/verify_phone'
        result_dict = self._rq.request('post', uri,
                                       post_data={'phone': phone_number, 'code': verification_code})
        if result_dict.get('verified', False) is True:
            return result_dict.get('verified_phone_token')
        return None

    def verify_phone_for_user(self, user_id, phone_number, verification_code):
        uri = '/users/%s/verify_phone_for_user' % user_id
        result_dict = self._rq.request('post', uri,
                                       post_data={'phone': phone_number, 'code': verification_code})
        return result_dict.get('verified', False) is True

    def request_email_verification_code(self, email_address):
        uri = '/users/request_email_verification_code'
        self._rq.request('post', uri, post_data={'email': email_address})

    def verify_email(self, email_address, verification_code):
        uri = '/users/verify_email'
        result_dict = self._rq.request('post', uri,
                                       post_data={'email': email_address, 'code': verification_code})
        if result_dict.get('verified', False) is True:
            return result_dict.get('verified_email_token')
        return None

    def verify_email_for_user(self, user_id, email_address, verification_code):
        uri = '/users/%s/verify_email_for_user' % user_id
        result_dict = self._rq.request('post', uri,
                                       post_data={'email': email_address, 'code': verification_code})
        return result_dict.get('verified', False) is True

    def disable_user(self, user_id, disabled=True):
        uri = '/users/{}/disable'.format(user_id)
        result_dict = self._rq.request(
            'post', uri, post_data={'disabled': disabled})
        user = User(self._rq, **result_dict)
        return user

    def refresh_session(self, session_token, token_private=None):
        uri = '/users/auth_token'
        headers = {'X-User-Token': session_token}
        if token_private:
            headers['X-User-Token-Private'] = token_private

        result_dict = self._rq.request('get', uri,
                                       headers=headers)
        session = Session(**result_dict)
        return session
