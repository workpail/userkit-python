from base64 import b64encode
import urllib.request, urllib.parse, urllib.error
from . import error

import json
import requests
import textwrap


class Requestor:

    def __init__(self, api_key=None, api_base_url=None):
        self.api_key = api_key
        self.api_base_url = api_base_url

        self.authorization = None

    def __del__(self):
        self.api_key = None
        self.api_base_url = None
        self.authorization = None

    def create_headers(self, headers):
        if self.authorization is None:
            if ':' in self.api_key:
                # Old style key
                b64_key = b64encode(self.api_key.encode()).decode()
                self.authorization = 'Basic %s' % b64_key
            else:
                # New style, username part is always "api"
                b64_key = b64encode(b'api:%s' % self.api_key.encode()).decode()
                self.authorization = 'Basic %s' % b64_key

        request_headers = {
            'Authorization': self.authorization,
            'X-Escape': 'false',  # Don't escape returned JSON
        }

        if headers:
            request_headers.update(headers)
        return request_headers

    def request(self, method, uri, headers=None, uri_params=None, post_data=None):
        url = '%s%s' % (self.api_base_url, uri)
        headers = self.create_headers(headers)

        if uri_params:
            uri_params = urllib.parse.urlencode(uri_params)
            url = '%s?%s' % (url, uri_params)

        if method.upper() in ['POST', 'PUT', 'PATCH']:
            headers.update({'Content-Type': 'application/json'})
            post_data = json.dumps(post_data)

        try:
            result = requests.request(
                method, url, headers=headers, data=post_data, timeout=60)
        except Exception as e:
            raise error.APIConnectionError(message=self._request_error_msg(e))

        return self.process_response(result.content, result.status_code)

    @staticmethod
    def process_response(content, status_code):
        try:
            json_body = json.loads(content)
        except Exception as e:
            msg = 'Parse error: {0}. Status code: {1}'.format(e, status_code)
            raise error.UserKitError(message=msg)

        if status_code == 200:
            return json_body
        elif status_code == 401:
            raise error.AppAuthenticationError(json_body=json_body)
        elif status_code == 400:
            if json_body['error'].get('type') == 'user_authentication_error':
                raise error.UserAuthenticationError(json_body=json_body)
            elif json_body['error'].get('type') == 'resource_not_found_error':
                raise error.ResourceNotFoundError(json_body=json_body)
            else:
                raise error.InvalidRequestError(json_body=json_body)
        elif status_code == 415:
            raise error.InvalidRequestError(json_body=json_body)
        else:
            msg = ('There was an error in our servers, status code: {}. '
                   'If this persists, please let us know at '
                   'support@userkit.io').format(status_code)
            raise error.APIError(message=msg)

    @staticmethod
    def _request_error_msg(e):
        if isinstance(e, requests.exceptions.RequestException):
            msg = ("Unexpected error communicating with UserKit.  "
                   "If this problem persists, let us know at "
                   "support@userkit.io.")
            err = "%s: %s" % (type(e).__name__, str(e))
        else:
            msg = ("Unexpected error communicating with UserKit. "
                   "It looks like there's probably a configuration "
                   "issue locally.  If this problem persists, let us "
                   "know at support@userkit.io.")
            err = "A %s was raised" % (type(e).__name__,)
            if str(e):
                err += " with error message %s" % (str(e),)
            else:
                err += " with no error message"
        msg = textwrap.fill(msg) + "\n\n(Network error: %s)" % (err,)
        return msg
