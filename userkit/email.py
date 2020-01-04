import json


class Email:
    _rq = None
    id = None
    to = None
    subject = None
    body = None

    def __init__(self, requestor, **kwargs):
        self._rq = requestor
        self.__dict__.update(kwargs)

    def __str__(self):
        return json.dumps(self.dict(), sort_keys=True, indent=2)

    def dict(self):
        return {k: v for k, v in self.__dict__.items()
                if not k.startswith('_') and not callable(v)}
