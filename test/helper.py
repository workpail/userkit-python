import json


DUMMY_USER = json.loads("""{
    "username": null,
    "auth_type": "password",
    "disabled": false,
    "id": "usr_j3LB5QPAH8B9UD",
    "verified_email": null,
    "name": "Jane Smith",
    "created": 1473559820.5583501,
    "last_failed_login": 1473894606.9857299,
    "last_login": 1474134570.0548699,
    "verified_phone": null,
    "email": "jane.smith@example.com"
}""")

DUMMY_USER_LIST = json.loads("""{
    "next_page": null,
    "users": [
        {
            "username": null,
            "auth_type": "password",
            "disabled": false,
            "id": "usr_TgTbetyiSvuiIw",
            "verified_email": null,
            "name": null,
            "created": 1473544359.3973701,
            "last_failed_login": null,
            "last_login": null,
            "verified_phone": null,
            "email": "jack.doe@example.com"
        },
        {
            "username": null,
            "auth_type": "password",
            "disabled": false,
            "id": "usr_j3LB5QPAH8B9UD",
            "verified_email": null,
            "name": "Jane Smith",
            "created": 1473559820.5583501,
            "last_failed_login": 1473894606.9857299,
            "last_login": 1474134570.0548699,
            "verified_phone": null,
            "email": "jane.smith@example.com"
        }
    ]
}""")

DUMMY_SESSION = json.loads("""{
    "token": "usr_j3LB5QPAH8B9UD:faketoken123123|sha256",
    "expires_in_secs": 86398.979590000003,
    "refresh_after_secs": 77758.979659999997
}""")

DUMMY_SUCCESS = json.loads("""{"success": true}""")

DUMMY_VERIFIED_PHONE_SUCCESS = json.loads("""{
    "verified": true,
    "verified_phone_token": "hIFg38faFhBLSx87fah9p"
}""")

DUMMY_VERIFIED_EMAIL_SUCCESS = json.loads("""{
    "verified": true,
    "verified_email_token": "aF9phIFghBfaLSx8h738f"
}""")

DUMMY_VERIFIED_EMAIL_OR_PHONE_FOR_USER_SUCCESS = json.loads(
    """{"verified": true}""")

DUMMY_INVITE_CREATE = json.loads("""{
    "token_raw": "invt_efmdqzGf32u77a-fli38NZGgR4jwU8gFDsq8KzV",
    "app_id": "app_6fa64vtE",
    "from_user": null,
    "accepted": false,
    "id": "invt_efmdqzGf32u77a",
    "expires_secs": 604800,
    "to_email": "anne.doe@example.com",
    "invite_url": "https://api.userkit.io/hosted_widget?app=app_6fa64vtE&amp;invt=invt_efmdqzGf32u77a-fli38NZGgR4jwU8gFDsq8KzV",
    "created": 1474248184.9626,
    "extras": null,
    "accepted_user": null,
    "accepted_date": null
}""")

DUMMY_INVITE = json.loads("""{
    "expires_secs": 604800,
    "to_email": "anne.doe@example.com",
    "accepted": false,
    "accepted_date": null,
    "created": 1474248184.9626,
    "accepted_user": null,
    "from_user": null,
    "id": "invt_efmdqzGf32u77a",
    "extras": null,
    "app_id": "app_6fa64vtE"
}""")

DUMMY_ACCEPTED_INVITE = json.loads("""{
    "expires_secs": 604800,
    "to_email": "james.doe@example.com",
    "accepted": true,
    "accepted_date": 1474297100.8381801,
    "created": 1474296046.0643599,
    "accepted_user": "usr_wojdQ286VOvSzA",
    "from_user": null,
    "id": "invt_y4GQk4GwfMFrlD",
    "extras": null,
    "app_id": "app_6fa64vtE"
}""")

DUMMY_INVITES_LIST = json.loads("""{
    "next_page": null,
    "invites": [
        {
            "expires_secs": 604800,
            "to_email": "anne.doe@example.com",
            "accepted": false,
            "accepted_date": null,
            "created": 1474248184.9626,
            "accepted_user": null,
            "from_user": null,
            "id": "invt_efmdqzGf32u77a",
            "extras": null,
            "app_id": "app_6fa64vtE"
        },
        {
            "expires_secs": 604800,
            "to_email": "james.doe@example.com",
            "accepted": false,
            "accepted_date": null,
            "created": 1474296046.0643599,
            "accepted_user": null,
            "from_user": null,
            "id": "invt_y4GQk4GwfMFrlD",
            "extras": null,
            "app_id": "app_6fa64vtE"
        }
    ]
}""")


class MockRequestor():
    """MockRequestor pretends to be the requestor.Requestor class.

    It returns the right kind of data for each API endpoint. For
    example a GET request to /users/<dummy-user-id> endpoint will
    return a user dict.
    """

    def request(self, method, uri, headers=None, uri_params=None, post_data=None):
        # Users -------------------------------------------------------

        # GET
        if method == 'get':
            # List users
            if uri == '/users':
                return DUMMY_USER_LIST
            # Refresh session token
            elif uri == '/users/auth_token':
                return DUMMY_SESSION
            # Get a user
            elif uri.startswith('/users/'):
                return DUMMY_USER

        # POST
        if method == 'post':

            if uri == '/users':
                return DUMMY_USER

            # Request phone verification, returns success flag
            elif uri == '/users/request_phone_verification_code':
                return DUMMY_SUCCESS

            # Request email verification, returns success flag
            elif uri == '/users/request_email_verification_code':
                return DUMMY_SUCCESS

            elif uri == '/users/request_password_reset':
                return DUMMY_SUCCESS

            elif uri == '/users/password_reset_new_password':
                return DUMMY_SUCCESS

            # Verify phone, returns verification-success token
            elif uri == '/users/verify_phone':
                return DUMMY_VERIFIED_PHONE_SUCCESS

            # Verify email, returns verification-success token
            elif uri == '/users/verify_email':
                return DUMMY_VERIFIED_EMAIL_SUCCESS

            # Login returns a session token
            elif uri == '/users/login':
                return DUMMY_SESSION

            # Logout returns a success flag
            elif uri == '/users/logout':
                return DUMMY_SUCCESS

            # User endpoints containing the DUMMY_USER's id
            elif uri.startswith('/users'):

                if DUMMY_USER['id'] in uri:

                    if uri.endswith('/disable'):
                        # This is a set-disabled state request, returns user
                        u = DUMMY_USER.copy()
                        u['disabled'] = post_data['disabled']
                        return u

                    elif uri.endswith('/auth_type'):
                        # This is a set-auth-type request, returns success flag
                        return DUMMY_SUCCESS

                    elif uri.endswith('/verify_phone_for_user'):
                        # Verify phone for user, returns verified success flag
                        return DUMMY_VERIFIED_EMAIL_OR_PHONE_FOR_USER_SUCCESS

                    elif uri.endswith('/verify_email_for_user'):
                        # Verify email for user, returns verified success flag
                        return DUMMY_VERIFIED_EMAIL_OR_PHONE_FOR_USER_SUCCESS

                    elif uri.endswith(DUMMY_USER['id']):
                        # This is an update
                        u = DUMMY_USER.copy()
                        u.update(post_data)
                        return u

        # Invites -----------------------------------------------------

        if uri.startswith('/invites'):

            if uri == '/invites':
                if method == 'post':
                    return DUMMY_INVITE_CREATE
                elif method == 'get':
                    return DUMMY_INVITES_LIST

            elif uri == '/invites/send' and method == 'post':
                return DUMMY_INVITE

            elif uri == '/invites/accept' and method == 'post':
                return DUMMY_ACCEPTED_INVITE

            elif uri.endswith(DUMMY_INVITE['id']) and method == 'get':
                return DUMMY_INVITE

        raise ValueError("No matching URI.  %s: %s" % (method, uri))
