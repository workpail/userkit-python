import util


USR_MUTABLE_FIELDS = ['username', 'email', 'name', 'password', 'auth_type']


class User(object):
    # instance fields
    _rq = None
    id = None
    username = None
    email = None
    name = None
    password = None
    auth_type = None

    def __init__(self, requestor, **kwargs):
        self._rq = requestor
        self.__dict__.update(kwargs)

    def __str__(self):
        return util.json.dumps(self.dict(), sort_keys=True, indent=2)

    def dict(self):
        return {k: v for k, v in self.__dict__.iteritems()
                if not k.startswith('_') and not callable(v)}

    def update_dict(self, dict):
        self.__dict__.update(dict)

    def save(self):
        uri = '/users/%s' % self.id
        post_data = {}
        for field in USR_MUTABLE_FIELDS:
            if field in self.__dict__:
                post_data[field] = self.__dict__.get(field)

        result_dict = self._rq.request('post', uri, post_data=post_data)
        self.__dict__.update(result_dict)

    def disable(self, disable_mode):
        uri = '/users/%s/disable' % self.id

        result_dict = self._rq.request('post', uri, post_data={'disabled': disable_mode})
        self.__dict__.update(result_dict)
