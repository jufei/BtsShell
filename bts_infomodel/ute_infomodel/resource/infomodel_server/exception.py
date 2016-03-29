# -*- coding: utf-8 -*-
"""
:created on: 18-10-2013

:copyright: NSN
:author: Pawel Sabat
:contact: pawel.sabat@nsn.com
"""


class InfoModelException(Exception):
    """Base exception of InfoModel exceptions."""


class InfoModelTimeoutException(InfoModelException):
    """InfoModelTimeoutException is raised when timeout occurs."""


class InfoModelOperationException(InfoModelException):
    """InfoModelOperationException is raised when InfoModel executors have problems."""


class InfoModelOperationNotFoundException(InfoModelOperationException):
    """InfoModelOperationNotFoundException is raised when InfoModel operation is not found."""


class InfoModelOperationParameterNotFoundException(InfoModelOperationException):
    """InfoModelOperationParameterNotFoundException is raised when InfoModel operation parameter is not found."""


class InfoModelOperationParameterWrongTypeException(InfoModelOperationException):
    """InfoModelOperationParameterWrongTypeException is raised when InfoModel operation parameter type is wrong."""


class InfoModelConnectionException(InfoModelException):
    """InfoModelConnectionException is raised when connection problems appear."""


class InfoModelObjectNotFoundException(InfoModelException):
    """InfoModelObjectNotFoundException is raised when InfoModel object cannot be found."""


class InfoModelObjectParameterNotFoundException(InfoModelException):
    """InfoModelObjectParameterNotFoundException is raised when InfoModel object parameter not found."""


class InfoModelObjectIndexedParameterNotFoundException(InfoModelException):
    """InfoModelObjectIndexedParameterNotFoundException is raised when InfoModel object parameter with specified index not found."""


class InfoModelObjectsNotFoundException(InfoModelException):
    """InfoModelObjectNotFoundException is raised when InfoModel objects cannot be found."""


class InfoModelQueryException(InfoModelException):
    """InfoModelQueryException base exception for query model."""


class InfoModelQueryExpressionSyntaxException(InfoModelQueryException):
    """InfoModelQueryExpressionSyntaxException is raised when query expression has syntax errors."""


class InfoModelQueryTimeoutException(InfoModelQueryException):
    """InfoModelQueryTimeoutException is raised when when a query does not pass with a positive."""
