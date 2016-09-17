# The Session object containing the session token and some timestamps used internally
class Session(object):
    refresh_after_secs = None
    expires_in_secs = None
    token = None

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def __str__(self):
        return '\ntoken: %s\nexpires_in_secs: %s\nrefresh_after_secs: %s\n' % (self.token, self.expires_in_secs, self.refresh_after_secs);
