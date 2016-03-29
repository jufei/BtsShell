# -*- coding: utf-8 -*-
"""
:created on: 04.03.14

:copyright: Nokia Solutions and Networks
:author: Bartłomiej Idzikowski
:contact: bartlomiej.idzikowski@nsn.com
"""


from time import time
from infomodel_server.exception import InfoModelQueryTimeoutException


def query_timeout(function):
    """Query timeout decorator"""

    def _wrap(inst, *args, **kwargs):
        timeout = kwargs.get('timeout', args[-1])
        operation_timeout = timeout
        expression = kwargs.get('query', args[-2]).expression
        return_value = None
        start_time, end_time = time(), time()
        while not return_value:
            start_time = time()
            return_value = function(inst, *args, **kwargs)
            end_time = time()
            timeout = timeout - (time() - start_time)
            if not return_value and timeout < 0.0:
                raise InfoModelQueryTimeoutException("query: '%s' doesn't pass with positive result in timeout=%s" % (expression, operation_timeout))

        return (return_value, start_time, end_time)
    return _wrap
