# -*- coding: utf-8 -*-
"""
:created on: 12.03.14

:copyright: Nokia Solutions and Networks
:author: Bartłomiej Idzikowski
:contact: bartlomiej.idzikowski@nsn.com
"""

import subprocess
import Pyro4

from bts_infomodel.ute_infomodel.util import ProcessControl


Pyro4.config.SERIALIZERS_ACCEPTED.add('pickle')
Pyro4.config.SERIALIZER = 'pickle'
Pyro4.config.SOCK_REUSE = True


class NameServerManager(object):

    def __init__(self, name_server_cli_dir):
        self.name_server_cli_dir = name_server_cli_dir

    def start(self):
        """Start Pyro4 name server."""
        # _logger.debug('Starting Pyro4 name server.')
        cmd = 'python nameserver.py'
        self.name_server_process = subprocess.Popen(cmd.split(), cwd=self.name_server_cli_dir)

    def stop(self):
        """Stop Pyro4 name server."""
        # _logger.debug("Pyro4 name server stoping.")
        ProcessControl(self.name_server_process).stop_process()


if __name__ == '__main__':
    try:
        nameserverUri, nameserverDaemon, broadcastServer = Pyro4.naming.startNS(enableBroadcast=False)
        nameserverDaemon.requestLoop()
    except:
        # print 'An Naming Server already Exist'
        pass
    finally:
        pass
