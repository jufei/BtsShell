# -*- coding: utf-8 -*-
"""
:created on: 06-12-2013

:copyright: NSN
:author: Bartłomiej Idzikowski
:contact: bartlomiej.idzikowski@nsn.com
"""


from ute_core.exception import CoreException
from .util import logger as _logger
from .exception import InfoModelUnexpectedException
from infomodel_server.exception import InfoModelException


def exception_handler(function):
    """Exception handler."""

    def _wrap(inst, *args, **kwargs):
        try:
            return function(inst, *args, **kwargs)
        except (InfoModelException, CoreException) as e:
            raise e
        except Exception, e:
            _logger.error("{}: {}".format(type(e), e))
            raise InfoModelUnexpectedException("Problem is unknown. {}: {}".format(type(e), e))
    return _wrap
