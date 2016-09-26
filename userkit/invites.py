from invite import Invite
import error


class InviteList(list):
    next_page = None


class InviteManager(object):
    _NQ = None

    def __init__(self, nq):
        self._NQ = nq

    def create_invite(self, **kwargs):
        post_data = {}
        for field in Invite._create_fields:
            if field in kwargs:
                post_data[field] = kwargs[field]

        uri = '/invites'
        result_dict = self._NQ.request('post', uri, post_data=post_data)
        iv = Invite(self._NQ, **result_dict)
        return iv

    def send_invite(self, **kwargs):
        post_data = {}
        for field in Invite._create_fields:
            if field in kwargs:
                post_data[field] = kwargs[field]

        uri = '/invites/send'
        result_dict = self._NQ.request('post', uri, post_data=post_data)
        iv = Invite(self._NQ, **result_dict)
        return iv

    def get_invite(self, invite_id):
        uri = '/invites/%s' % invite_id
        try:
            result_dict = self._NQ.request('get', uri)
        except error.ResourceNotFoundError:
            return None
        iv = Invite(self._NQ, **result_dict)
        return iv

    def get_invites(self, limit=25, next_page=None):
        uri_params = {}
        if limit:
            uri_params['limit'] = limit
        if next_page:
            uri_params['next_page'] = next_page

        uri = '/invites'
        result_list = self._NQ.request('get', uri, uri_params=uri_params)

        invite_list = InviteList()
        for invite_dict in result_list.get('invites', []):
            invite_list.append(Invite(self._NQ, **invite_dict))

        invite_list.next_page = result_list.get('next_page')
        return invite_list

    def accept_invite(self, user_id, token):
        uri = '/invites/accept'
        result_dict = self._NQ.request(
            'post', uri, post_data={'user_id': user_id, 'token': token})
        iv = Invite(self._NQ, **result_dict)
        return iv
