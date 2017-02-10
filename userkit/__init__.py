from requestor import Requestor
from users import UserManager
from invites import InviteManager
from emails import EmailManager
from session import Session
from widget import WidgetManager


class UserKit(object):
    _rq = None
    api_version = 1.0
    api_base_url = None
    api_key = None
    users = None
    invites = None
    emails = None
    widget = None

    def __init__(self, api_key, api_base_url=None, _requestor=None):
        if api_key is None:
            raise TypeError('api_key cannot be blank.')

        if api_base_url is None:
            api_base_url = 'https://api.userkit.io/v1'
        else:
            api_base_url += '/v1'

        self.api_key = api_key
        self.api_base_url = api_base_url

        # make the encapsulated objects
        self._rq = _requestor or Requestor(self.api_key, self.api_base_url)
        self.users = UserManager(self._rq)
        self.invites = InviteManager(self._rq)
        self.emails = EmailManager(self._rq)
        self.widget = WidgetManager(self._rq)

    @classmethod
    def version(cls):
        return cls.api_version
