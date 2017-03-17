import util


LOG_CREATE_FIELDS = ['actor', 'actor_ip', 'actor_useragent', 'action', 'actee', 'details']


class Log(object):
    # instance vars
    id = None
    action = None
    details = None

    request = None
    request_ip = None

    actor = None
    actor_app = None
    actor_session = None
    actor_ip = None
    actor_useragent = None
    actor_location = None

    actee = None
    actee_app = None

    occurred = None

    def __init__(self, requestor, **kwargs):
        self._rq = requestor
        self.__dict__.update(kwargs)

    def __str__(self):
        return util.json.dumps(self.dict(), sort_keys=True, indent=2)

    def dict(self):
        return {k: v for k, v in self.__dict__.iteritems()
                if not k.startswith('_') and not callable(v)}
