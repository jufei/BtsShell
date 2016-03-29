# -*- coding: utf-8 -*-
"""
:created on: 24-02-2014

:copyright: NSN
:author: Bartłomiej Idzikowski
:contact: bartlomiej.idzikowski@nsn.com
"""


import threading
from time import time
from .exception import InfoModelConnectionException, InfoModelTimeoutException


class ConnectionStatus(object):
    STARTED = "Started"
    CONNECTED = "Connected"
    FOUND_INFOMODEL = "FoundInfoModel"
    REGISTERED_TO_INFOMODEL = "RegisteredToInfoModel"
    DISCONNECTED = "Disconnected"
    RECONNECTING = "Reconnecting"


class ModelAction(object):
    ON_RESET = 'onReset'
    ON_REMOVE = 'onRemove'
    ON_CHANGE = 'onChange'


class ConnectionManager(object):

    def __init__(self):
        self.status = None
        self.condition = threading.Condition()

    def notify(self, event):
        """Called when connection status changes."""
        self.status = str(event.getType())
        self.condition.acquire()
        self.condition.notify()
        self.condition.release()

    def is_status_reached(self, status):
        """Check that status is reached."""
        return self.status == status

    def wait_for_status(self, status, timeout=0):
        """Wait for specified status."""
        self.condition.acquire()
        start_time = time()
        while not self.is_status_reached(status) and time() - start_time <= timeout:
            self.condition.wait(timeout - (time() - start_time))
        self.condition.release()

        if self.is_status_reached(status):
            return True
        raise InfoModelConnectionException('Expected connection status: %s not achieved. Status reached: %s' % (status, self.status))


class ModelChangeManager(object):
    def __init__(self):
        self.condition = threading.Condition()
        self.action = None
        self.data = None
        self.timestamp = None

    def notify(self, event):
        """Called when model is changed."""
        self.action, self.data, self.timestamp = event
        self.condition.acquire()
        self.condition.notify()
        self.condition.release()

    def wait_for_action(self, action, timeout):
        """Wait for specified action.

        :param string action: InfoModel action.
        :param float timeout: Waiting time for this operation.
        """
        self.condition.acquire()
        start_time = time()
        while self.action != action and time() - start_time <= timeout:
            self.condition.wait(timeout - (time() - start_time))
        self.condition.release()
        if self.action == action:
            return True
        raise InfoModelTimeoutException('Expected: %s action on InfoModel not registered.' % action)

    def wait_for_any_action(self, timeout):
        """Wait for any action."""
        self.condition.acquire()
        start_time = time()
        while self.action is None and time() - start_time <= timeout:
            self.condition.wait(timeout)
        self.condition.release()
        if self.action is not None:
            return True
        raise InfoModelTimeoutException('No action (change|remove|reset) on InfoModel registered.')

    def wait_for_change(self, timeout):
        """"Wait for onChange action."""
        return self.wait_for_action(ModelAction.ON_CHANGE, timeout)

    def wait_for_remove(self, timeout):
        """Wait for onRemove action."""
        return self.wait_for_action(ModelAction.ON_REMOVE, timeout)

    def wait_for_reset(self, timeout):
        """Wait for onReset action."""
        return self.wait_for_action(ModelAction.ON_RESET, timeout)
