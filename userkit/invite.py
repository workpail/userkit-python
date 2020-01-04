import json


INVT_CREATE_FIELDS = ['to_email', 'from_user', 'expires_secs', 'extras',
                      'greeting', 'body', 'signature']


class Invite:
    # instance vars
    id = None
    token = None
    _rq = None
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

    def __init__(self, requestor, **kwargs):
        self._rq = requestor
        self.__dict__.update(kwargs)

    def __str__(self):
        return json.dumps(self.dict(), sort_keys=True, indent=2)

    def dict(self):
        return {k: v for k, v in self.__dict__.items()
                if not k.startswith('_') and not callable(v)}
