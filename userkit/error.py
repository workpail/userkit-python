"""
UserKit errors
"""


class CoreError(Exception):
    """Base UserKit exception class"""

    type = None
    code = None
    param = None
    message = None
    retry_wait = None

    def __init__(self, json_obj=None, message=None):
        msg = message
        if json_obj and not msg:
            msg = json_obj.get('message')
        super(CoreError, self).__init__(msg)

        if json_obj:
            err = json_obj.get('error')
            self.type = err.get('type')
            self.code = err.get('code')
            self.param = err.get('param')
            self.message = msg
            self.retry_wait = err.get('retry_wait')

    def __unicode__(self):
        return self.message


class UserKitError(CoreError):

    # Some endpoints return a list of multiple errors
    errors = []

    def __init__(self, json_obj=None, message=None):
        super(UserKitError, self).__init__(json_obj=json_obj, message=message)

        if json_obj:
            errs = json_obj.get('errors', [])
            for e in errs:
                self.errors.append(CoreError(e))


class AppAuthenticationError(UserKitError):
    """Unable to authenticate the userkit app making the request"""
    pass


class APIError(UserKitError):
    pass


class APIConnectionError(APIError):
    pass


class InvalidRequestError(UserKitError):
    pass


class UserError(UserKitError):
    pass


class UserAuthenticationError(UserError):
    """Unable to authenticate the user. E.g. bad login or session"""
    pass


class ResourceNotFoundError(UserKitError):
    """The requested resource (ie. user, invite) doesn't exist"""
    pass
