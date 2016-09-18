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


class MockRequestor(object):
    """MockRequestor pretends to be the requestor.Requestor class.

    It returns the right kind of data for each API endpoint. For
    example a GET request to /users/<user-id> endpoint will return a
    user dict.
    """

    def request(self, method, uri, headers=None, uri_params=None, post_data=None):
        # GET
        if method == 'get':
            # List users
            if uri == '/v1/users':
                return DUMMY_USER_LIST
            # Get a user
            elif uri.startswith('/v1/users/'):
                return DUMMY_USER

        # POST
        if method == 'post':
            # Login returns a session token
            if uri == '/v1/users/login':
                return DUMMY_SESSION
            # Create and update endpoints both return a user
            elif uri.startswith('/v1/users'):
                return DUMMY_USER
