# -*- coding: utf-8 -*-
"""
:created on: 03-12-2013

:copyright: NSN
:author: Tomasz Kolek
:contact: tomasz.kolek@nsn.com
"""

import traceback
from time import time
from .manager import ConnectionStatus
from infomodel_server.exception import InfoModelException
from infomodel_server.util import logger as _logger


def exception_handler(function):
    """Handler of server exceptions."""

    def _wrap(inst, *args, **kwargs):
        try:
            return function(inst, *args, **kwargs)
        except InfoModelException as e:
            raise e
        except Exception as e:
            _logger.error(str(e))
            raise InfoModelException("%s\n%s" % (str(e), traceback.format_exc()))
    return _wrap


def check_connection_status(function):
    """Check connection status."""
    def _wrap(inst, *args, **kwargs):
            timeout = kwargs.get('timeout', args[-1])
            inst.model.connection_manager.wait_for_status(ConnectionStatus.REGISTERED_TO_INFOMODEL, timeout)
            return function(inst, *args, **kwargs)
    return _wrap
