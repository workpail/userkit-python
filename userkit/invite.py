class Invite(object):
    # class vars
    mutable_fields = ['to_email', 'from_user', 'expires_secs', 'extras',
                      'greeting', 'body', 'signature']

    # instance vars
    id = None
    token = None
    _NQ = None
    accepted = None
    accepted_date = None
    accepted_user = None
    app_id = None
    created = None
    expires_secs = None
    extras = None
    from_user = None
    to_email = None
    token_raw = None
    invite_url = None

    def __init__(self, nq, **kwargs):
        self._NQ = nq
        self.__dict__.update(kwargs)

    def __str__(self):
        rs = ''
        klist = sorted(self.__dict__.keys())
        for key in klist:
            if rs is not '':
                rs += ', '
            rs += "'%s': '%s'" % (key, self.__dict__[key])
        return '{' + rs + '}'
