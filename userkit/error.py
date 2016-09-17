# Portions of this software were based on and incorporate the open
# sourced MIT Licensed version of Stripe

# The MIT License
#
# Copyright (c) 2010-2011 Stripe (http://stripe.com)
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.


# Generic Base Error
class Error(Exception):
    def __init__(self, error_obj=None, code=None, param=None, message=None, http_status=None, http_body=None):
        super(Error, self).__init__(str(message))
        self.error_obj = error_obj
        self.code = code
        self.param = param
        self.http_status = http_status
        self.http_body = http_body

    def __repr__(self):
        return str(self.__class__.__name__) + '( error_obj=' + str(self.error_obj) + ', code=\'' + str(self.code) + '\', param=\'' + str(self.param) + '\' , message=\'' + str(self.message) + '\', http_status=' + str(self.http_status) + ', http_body=\'' + str(self.http_body) + '\')'

    def to_dict(self):
        return {
                'error_obj': self.error_obj,
                'code': str(self.code),
                'param': str(self.param),
                'message': str(self.message),
                'http_status': self.http_status,
                'http_body': str(self.http_body)
        }

class MissingAPIKey(Error):
    pass

class ErrorsList(Error):
    def __init__(self, error_obj_list=None, message=None, http_status=None, http_body=None):
        self.errors_list = error_obj_list or []
        self.http_status = http_status
        self.http_body = http_body

    def append(self, error_obj):
        self.errors_list.append(error_obj)

    def to_dict(self):
        out = []
        for error in self.errors_list:
            out.append(error.to_dict())
        return out

    def __str__(self):
        out = []
        for error in self.errors_list:
            out.append(str(error))
        return str(self.__class__.__name__) + '(\n\t' + ',\n\t'.join(out) + '\n)'

    def __iter__(self):
        for error in self.errors_list:
            yield error

class HTTPError(Error):
    def __init__(self, message=None, http_status=None, http_body=None):
        super(HTTPError, self).__init__(message='http_status: %s, http_body: %s' % (str(http_status), str(http_body)))
        self.error_obj = str(message)
        self.code = None
        self.param = None
        self.http_status = http_status
        self.http_body = http_body


class ParseError(Error):
    pass


class APIError(Error):
    pass


class APIConnectionError(APIError):
    pass


class RequestError(Error):
    pass

class InvalidRequestError(RequestError):
    pass


### User Errors ###

class UserError(Error):
    def __new__(cls, error_obj, code=None, param=None, message=None, http_status=None, http_body=None):
        if (code == 'unauthorized') or (error_obj.get('code') == 'unauthorized'):
            return super(UserError, cls).__new__(RequiresLoginError, error_obj=error_obj, code=code, param=param, message=message, http_status=http_status, http_body=http_body)

        return super(UserError, cls).__new__(UserError, error_obj=error_obj, code=code, param=param, message=message, http_status=http_status, http_body=http_body)

class RequiresLoginError(UserError):
    pass



### Helper functions to create the appropriate error exception ###

error_types = {
    'user_error': UserError,
    'requires_login': RequiresLoginError,
    'api_error': APIError,
    'invalid_request_error': InvalidRequestError,
    'json_parse_error': ParseError,
    'http_error': HTTPError,
    '*': Error
}


def error_by_type(error_type, message=None, http_status=None, http_body=None):
    if not error_type:
        return error_types['*'](message=message, http_status=http_status, http_body=http_body)
    
    if not error_types.has_key(error_type):
        return error_types['*'](message=message, http_status=http_status, http_body=http_body)

    return error_types[error_type](message=message, http_status=http_status, http_body=http_body)


def error_by_obj(error_obj, message=None, http_status=None, http_body=None):
    if not error_obj:
        return error_by_type('missing_error_obj', message=message, http_status=http_status, http_body=http_body)

    error_type = error_obj.get('type')
    if not message:
        message = error_obj.get('message')

    code = error_obj.get('code')
    param = error_obj.get('param')

    if error_types.has_key(error_type):
        return error_types[error_type](error_obj=error_obj, code=code, param=param, message=message, http_status=http_status, http_body=http_body)

    return error_types['*'](error_obj=error_obj, code=code, param=param, message=message, http_status=http_status, http_body=http_body)


def error_by_obj_list(error_obj_list, message=None, http_status=None, http_body=None):
    errors = ErrorsList(message=None, http_status=None, http_body=None)
    for err_obj in error_obj_list:
        errors.append(error_by_obj(err_obj.get('error', err_obj)))
    return errors

