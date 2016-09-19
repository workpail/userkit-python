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
            self.authorization = 'Basic %s' % (base64.b64encode('%s' % self.api_key))

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
        if status_code == 200:
            try:
                return util.json.loads(content)
            except Exception as e:
                raise error.error_by_type('json_parse_error', message=repr(e),
                                    http_status=status_code, http_body=content)

        elif status_code == 404 or status_code == 500:
            raise error.error_by_type('http_error', http_status=status_code,
                                      http_body=content)

        # otherwise we have an error condition
        try:
            jsonOb = util.json.loads(content)
        except Exception as e:
            raise error.error_by_type('json_parse_error', message=repr(e),
                                      http_status=status_code, http_body=content)

        # otherwise, a non-200 code was returned along with a JSON error object
        if jsonOb.get('error'):
            raise error.error_by_obj(jsonOb.get('error'),
                                http_status=status_code, http_body=content)
        elif jsonOb.get('errors'):
            raise error.error_by_obj_list(jsonOb.get('errors'),
                                http_status=status_code, http_body=content)
        else:
            raise error.error_by_type('api_error',
                                      message='No Error Object Returned',
                                      http_status=status_code,
                                      http_body=content)
