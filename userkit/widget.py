import json


class ProxyResponse:
    """Holds the response data for a widget-proxy request.

    response:
        The response data a JSON string, ready to pass back to the
        widget.
    response_dict:
        The response data as a dict.
    token_private:
        The private-token, which can be used as an http-only cookie
        value.
    """
    response = None
    response_dict = None
    token_private = None


class WidgetManager:
    _rq = None

    def __init__(self, requestor):
        self._rq = requestor

    def proxy(self, body, token_private=None, ip=None):
        """
        Make a request to the widget proxy endpoint.

        :param body:
            The request body from the widget. Can be either a JSON
            string or a dictionary.
        :param token_private:
            The session private token, from an http-only cookie.
        :return:
            Returns a ProxyResponse object. This object contains
            response data which should be returned to the widget.
        """
        uri = '/widget/proxy'
        content = {}

        # body can be either a JSON string, or dict
        if isinstance(body, dict):
            content['data'] = body
        else:
            content['data'] = json.loads(body)

        if token_private:
            content['token_private'] = token_private

        if ip:
            content['ip'] = ip

        result_dict = self._rq.request('post', uri, post_data=content)
        resp = ProxyResponse()
        resp.response = json.dumps(result_dict.get('response'))
        resp.response_dict = result_dict.get('response')
        resp.token_private = result_dict.get('token_private')
        return resp
