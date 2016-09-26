import base64
import urllib
import util
import error

from http_client import new_default_http_client


class Requestor(object):

    def __init__(self, api_key=None, api_base_url=None):
        self.api_key = api_key
        self.api_base_url = api_base_url

        # we create ONE instance of an http handler
        self.authorization = None
        self.httpHandler = new_default_http_client()

    def __del__(self):
        self.api_key = None
        self.api_base_url = None
        self.authorization = None

    def create_headers(self, headers):
        if self.authorization is None:
            if ':' in self.api_key:
                # Old style key
                self.authorization = 'Basic %s' % \
                                     base64.b64encode('%s' % self.api_key)
            else:
                # New style, username part is always "api"
                self.authorization = 'Basic %s' % \
                                     base64.b64encode('api:%s' % self.api_key)

        request_headers = {
            'Authorization': self.authorization
        }

        if headers:
            request_headers.update(headers)
        return request_headers

    def request(self, method, uri, headers=None, uri_params=None, post_data=None):
        url = '%s%s' % (self.api_base_url, uri)
        headers = self.create_headers(headers)

        if uri_params:
            uri_params = urllib.urlencode(uri_params)
            url = '%s?%s' % (url, uri_params)

        if method.upper() in ['POST', 'PUT', 'PATCH']:
            headers.update({'Content-Type': 'application/json'})
            post_data = util.json.dumps(post_data)

        content, status_code = self.httpHandler.request(method, url, headers,
                                                        post_data)

        return self.process_response(content, status_code)

    def process_response(self, content, status_code):
        try:
            json_body = util.json.loads(content)
        except Exception as e:
            msg = 'Parse error: {0}. Status code: {1}'.format(e, status_code)
            raise error.UserKitError(message=msg)

        if status_code == 200:
            return json_body
        elif status_code == 401:
            raise error.AppAuthenticationError(json_obj=json_body)
        elif status_code == 400:
            if json_body['error'].get('type') == 'user_error':
                if json_body['error'].get('code') == 'unauthorized':
                    raise error.UserAuthenticationError(json_obj=json_body)
                else:
                    raise error.UserError(json_obj=json_body)
            elif json_body['error'].get('code') == 'not_found':
                raise error.ResourceNotFoundError(json_obj=json_body)
            else:
                raise error.InvalidRequestError(json_obj=json_body)
        elif status_code == 415:
            raise error.InvalidRequestError(json_obj=json_body)
        else:
            msg = ('There was an error in our servers, status code: {}. '
                   'If this persists, please let us know at '
                   'support@userkit.io').format(status_code)
            raise error.APIError(message=msg)
