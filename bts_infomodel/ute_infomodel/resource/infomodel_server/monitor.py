#!/usr/bin/env jython
# -*- coding: utf-8 -*-
"""
:created on: 30-07-2013

:copyright: NSN
:author: Bartłomiej Idzikowski
:contact: bartlomiej.idzikowski@nsn.com
"""


from com.nsn.oam.infomodel.communication import InfoModelListener
from com.nsn.oam.infomodel.communication.network import ConnectionStatusListener

from .util import logger
from .observer import Observable
from .manager import ModelAction


class ModelChangeMonitor(InfoModelListener, Observable):
    def __init__(self):
        Observable.__init__(self)

    def onRemove(self, removed, timestamp):
        """Called when infomodel object is removed."""
        self.notify_all((ModelAction.ON_REMOVE, removed, timestamp))

    def onReset(self, timestamp):
        """Called when connection reset."""
        self.notify_all((ModelAction.ON_RESET, None, timestamp))

    def onChange(self, changed, timestamp):
        """Called when infomodel object changes."""
        self.notify_all((ModelAction.ON_CHANGE, changed, timestamp))


class ConnectionStatusChangeMonitor(ConnectionStatusListener, Observable):
    def __init__(self):
        Observable.__init__(self)

    def onConnectionStatusChanged(self, event):
        """This method is called when connetion changes."""
        self.notify_all(event)
