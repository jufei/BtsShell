# -*- coding: utf-8 -*-
"""
:created on: 10-12-2013

:copyright: NSN
:author: Bartłomiej Idzikowski
:contact: bartlomiej.idzikowski@nsn.com
"""


import logging
import subprocess
import sys
import Pyro4
from time import time, sleep
from .exception import InfoModelUnexpectedException

logger = logging.getLogger(__file__)
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)

_logger = logger
Pyro4.config.SERIALIZERS_ACCEPTED.add('pickle')
Pyro4.config.SERIALIZER = 'pickle'


def find_name_server(timeout=120):
    """Find Pyro4 name server."""
    start_time = time()
    name_server = None
    _logger.debug('Finding Pyro4 name server.')
    while not name_server and time() - start_time <= timeout:
        try:
            name_server = Pyro4.naming.locateNS()
        except Exception:
            sleep(1)

    if name_server:
        _logger.debug('Pyro4 name server found.')
        return name_server

    _logger.debug('Pyro4 name server not found.')
    raise InfoModelUnexpectedException("Pyro4 name server not found.")


def find_service(name_server, service_name, timeout=180):
    """Find service registered in Pyro4 name server."""
    start_time = time()
    service_uri = None
    _logger.debug('Finding service: %s' % service_name)
    while not service_uri and time() - start_time <= timeout:
        try:
            service_uri = name_server.lookup(service_name)
        except Exception as e:
            service_uri = None
            sleep(1)

    if service_uri:
        _logger.debug("Service: %s found." % service_name)
        return service_uri

    _logger.debug('Service: %s not found.' % service_name)
    raise InfoModelUnexpectedException("Service: %s not found." % service_name)


class ProcessControl(object):
    def __init__(self, process):
        self.process = process

    def stop_process(self):
        """Stop subprocess process"""
        if self.process and not self._is_process_terminated():
            self.process.terminate()
            if not self._process_terminates_within(5):
                self.process.kill()

    def _process_terminates_within(self, timeout):
        return self._wait(self._is_process_terminated, 0.25, timeout)

    def _is_process_terminated(self):
        return self.process.poll() is not None

    def _wait(self, cond_func, sleep_step, timeout):
        start = time()
        while not cond_func():
            now = time()
            if now - start >= timeout:
                return False
            sleep(sleep_step)
        return True


def turn_on_echo():
    """Turn on echo by running stty echo command"""
    if sys.platform.startswith('linux'):
        cmd = ['stty', 'echo']
        subprocess.call(cmd)
