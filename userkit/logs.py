from log import Log, LOG_CREATE_FIELDS


class LogsList(list):
    next_page = None


class LogsManager(object):
    _rq = None

    def __init__(self, requestor):
        self._rq = requestor

    def log_event(self, **kwargs):
        post_data = {}
        for field in LOG_CREATE_FIELDS:
            if field in kwargs:
                post_data[field] = kwargs[field]

        uri = '/audits'
        result_dict = self._rq.request('post', uri, post_data=post_data)
        log = Log(self._rq, **result_dict)
        return log

