from .email import Email
from . import error


class EmailManager:
    _rq = None

    def __init__(self, requestor):
        self._rq = requestor

    def get_pending_email(self, email_key):
        uri = '/emails/pending'
        headers = {'X-Email-Key': email_key}
        try:
            result_dict = self._rq.request('get', uri, headers=headers)
        except error.ResourceNotFoundError:
            return None
        eml = Email(self._rq, **result_dict)
        return eml
