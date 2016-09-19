import util


class Session(object):
    """Session holds a user's session info.

    login_user() and refresh_token() return a Session object.
    """
    refresh_after_secs = None
    expires_in_secs = None
    token = None

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def __str__(self):
        return util.json.dumps(self.dict(), sort_keys=True, indent=2)

    def dict(self):
        return {k: v for k, v in self.__dict__.iteritems()
                if not k.startswith('_') and not callable(v)}
