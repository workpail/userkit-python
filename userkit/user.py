class User(object):
    # class field
    mutable_fields = ['username', 'email', 'name', 'password', 'auth_type']

    # instance fields
    _NQ = None
    id = None
    username = None
    email = None
    name = None
    password = None
    auth_type = None

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

    def dict(self):
        rsDict = {}
        for key, value in self.__dict__.iteritems():
            if not key.startswith('__') and (key != '_NQ') and not callable(value):
                rsDict[key] = value
        return rsDict

    def update_dict(self, dict):
        self.__dict__.update(dict)

    def save(self):
        uri = '/v1/users/%s' % self.id
        post_data = {}
        for field in self.mutable_fields:
            val = self.__dict__.get(field)
            if val is not None:
                post_data[field] = val

        result_dict = self._NQ.request('post', uri, post_data=post_data)
        self.__dict__.update(result_dict)
        return True

    def disable(self, disable_mode):
        uri = '/v1/users/%s/disable' % self.id

        result_dict = self._NQ.request('post', uri, post_data={'disabled' : disable_mode})
        self.__dict__.update(result_dict)
        return True
