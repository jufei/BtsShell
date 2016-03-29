# -*- coding: utf-8 -*-
"""
:created on: 24-02-2014

:copyright: NSN
:author: Bartłomiej Idzikowski
:contact: bartlomiej.idzikowski@nsn.com
"""


from v1.executor import QueryExecutor as QueryExecutorAPI_V1


class QueryExecutorFactory(object):
    QUERY_API = {'v1': QueryExecutorAPI_V1}

    def __new__(cls, api_version, model):
        return QueryExecutorFactory.QUERY_API[api_version](model)
