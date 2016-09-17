from user import User
from session import Session
import error as error


class UserList(list):
    next_page = None


class UserManager(object):
    _NQ = None
    validAuthTypes = ['OTP', '2FA', 'password']
    validSendTypes = ['sms', 'call']

    def __init__(self, nq):
        self._NQ = nq

    def is_valid_auth_type(self, auth_type):
        return auth_type in UserManager.validAuthTypes

    def is_valid_send_type(self, send_type):
        return send_type in UserManager.validSendTypes

    def get_current_user(self, token):
        if not token:
            return None
        try:
            return self.fetch_user_by_token(token)
        except error.RequiresLoginError:
            return None

    def create_user(self, **kwargs):
        if not kwargs:
            return None

        post_data = {}
        for field in User.mutable_fields:
            if (kwargs.has_key(field) and (kwargs.get(field) is not None)):
                post_data[field] = kwargs.get(field)

        uri = '/v1/users'
        result_dict = self._NQ.request('post', uri, post_data=post_data)
        user = User(self._NQ, **result_dict)
        return user

    def login_user(self, username, password, tfcode=None):
        if not username or not password:
            return None

        post_data = {'username': username, 'password': password}
        if tfcode:
            post_data['code'] = tfcode

        uri = '/v1/users/login'
        result_dict = self._NQ.request('post', uri, post_data=post_data)

        session = Session(**result_dict)
        return session

    def logout_user(self, token):
        if not token:
            return False

        uri = '/v1/users/logout'
        self._NQ.request('post', uri, headers={'X-User-Token': token})
        return True

    def fetch_user_by_token(self, token):
        if not token:
            return None

        uri = '/v1/users/by_token'
        result_dict = self._NQ.request('get', uri, headers={'X-User-Token': token})
        user = User(self._NQ, **result_dict)
        return user

    def fetch_user_by_userid(self, user_id):
        if not user_id:
            return None

        uri = '/v1/users/%s' % user_id
        result_dict = self._NQ.request('get', uri)
        return User(self._NQ, **result_dict)

    def request_password_reset(self, username_or_email):
        if not username_or_email:
            return False

        try:
            uri = '/v1/users/request_password_reset'
            self._NQ.request('post', uri, post_data={'username_or_email': username_or_email})
            return True
        except error.ParseError:
            pass
        return False

    def reset_password(self, pw_reset_token, new_password):
        if not pw_reset_token or not new_password:
            return False

        try:
            uri = '/v1/users/password_reset_new_password'
            self._NQ.request('post', uri, post_data={'token': pw_reset_token, 'password': new_password})
            return True
        except error.ParseError:
            pass
        return False

    def fetch_all(self, limit=25, next_page=None, search=None, show_disabled=None):
        uri_params = {}
        if limit:
            uri_params['limit'] = limit
        if next_page:
            uri_params['next_page'] = next_page
        #js is this supported?
        # if search:
        #     uri_params["search"] = search
        # if show_disabled:
        #     uri_params["show_disabled"] = show_disabled

        uri = '/v1/users'
        result_list = self._NQ.request('get', uri, uri_params=uri_params)
        user_list = UserList()
        for user_dict in result_list.get('users', []):
            user = User(self._NQ, **user_dict)
            user_list.append(user)

        user_list.next_page = result_list.get('next_page')
        return user_list

    def assign_user_auth_type(self, user_id, auth_type, phone_number=None, phone_token=None):
        if not user_id or not self.is_valid_auth_type(auth_type):
            return False

        post_data = {'auth_type' : auth_type}
        if phone_number and phone_token:
            post_data['phone'] = phone_number
            post_data['phone_token'] = phone_token

        try:
            uri = '/v1/users/%s/auth_type' % user_id
            result_dict = self._NQ.request('post', uri, post_data=post_data)
            return result_dict.get('success', False) is True
        except error.ParseError:
            pass
        return False

    def request_phone_verification_code(self, phone_number, send_method):
        if not phone_number or not self.is_valid_send_type(send_method):
            return False

        try:
            uri = '/v1/users/request_phone_verification_code'
            result_dict = self._NQ.request('post', uri, post_data={'phone' : phone_number, 'send_method' : send_method})
            return result_dict.get('success', False) is True
        except error.ParseError:
            pass
        return False

    def verify_phone(self, phone_number, verification_code):
        if not phone_number or not verification_code:
            return None

        try:
            uri = '/v1/users/verify_phone'
            result_dict = self._NQ.request('post', uri, post_data={'phone' : phone_number, 'code' : verification_code})
            if result_dict.get('verified', False) is True:
                return result_dict.get('verified_phone_token')
            return None
        except error.ParseError:
            pass
        return None

    def verify_phone_for_user(self, user_id, phone_number, verification_code):
        if not user_id or not phone_number or not verification_code:
            return False

        try:
            uri = '/v1/users/%s/verify_phone_for_user' % user_id
            result_dict = self._NQ.request('post', uri, post_data={'phone' : phone_number, 'code' : verification_code})
            return result_dict.get('verified', False) is True
        except error.ParseError:
            pass
        return False

    def request_email_verification_code(self, email_address):
        if not email_address:
            return False

        try:
            uri = '/v1/users/request_email_verification_code'
            result_dict = self._NQ.request('post', uri, post_data={'email' : email_address})
            return result_dict.get('success', False) is True
        except error.ParseError:
            pass
        return False

    def verify_email(self, email_address, verification_code):
        if not email_address or not verification_code:
            return None

        try:
            uri = '/v1/users/verify_email'
            result_dict = self._NQ.request('post', uri, post_data={'email': email_address, 'code': verification_code})
            if result_dict.get('verified', False) is True:
                return result_dict.get('verified_email_token')
            return None
        except error.ParseError:
            pass
        return None

    def verify_email_for_user(self, user_id, email_address, verification_code):
        if not user_id or not email_address or not verification_code:
            return False

        try:
            uri = '/v1/users/%s/verify_email_for_user' % user_id
            result_dict = self._NQ.request('post', uri, post_data={'email': email_address, 'code': verification_code})
            return result_dict.get('verified', False) is True
        except error.ParseError:
            pass
        return False
