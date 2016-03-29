#!/usr/bin/env jython
# -*- coding: utf-8 -*-
"""
:created on: 30-07-2013

:copyright: NSN
:author: Bartłomiej Idzikowski
:contact: bartlomiej.idzikowski@nsn.com
"""

import sys
import argparse
import Pyro4

from infomodel_server.server import InfoModelServer
from infomodel_server.util import logger, find_name_server


Pyro4.config.SERIALIZERS_ACCEPTED.add('pickle')
Pyro4.config.SERIALIZER = 'pickle'


def _run_infomodel_server(params):
    try:
        infomodel_server = InfoModelServer(
            params.address,
            params.port,
            params.update_interval,
            params.auto_reconnect,
            params.definitions_file_path,
            params.ftp_port,
            params.ftp_username,
            params.ftp_password,
        )
        daemon = Pyro4.Daemon()
        ns = find_name_server()
        uri = daemon.register(infomodel_server)
        # logger.debug("InfoModel server uri: %s" % uri)  #comment by Jufei
        ns.register(params.service_name, uri)
        # logger.debug("InfoModel server ready.")   #comment by Jufei
        daemon.requestLoop(loopCondition=infomodel_server.is_running)
    except Exception, e:
        logger.error('Server error. Quiting... %s' % e)
        logger.error(str(e))
        sys.exit(1)
    finally:
        pass
        # logger.info('Server exit.')   #comment by Jufei


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()

    parser_server_run = subparsers.add_parser('run')
    parser_server_run.add_argument('--address', type=str, default='192.168.255.1', help='BTS ip address.')
    parser_server_run.add_argument('--port', type=int, default=15003, help='Port.')
    parser_server_run.add_argument('--update_interval', type=int, default=0, help='Update interval.')
    parser_server_run.add_argument('--auto_reconnect', action='store_true', help='Auto reconnect')
    parser_server_run.add_argument('--ftp_port', type=int, default=21, help='eNB ftp port.')
    parser_server_run.add_argument('--ftp_username', type=str, default='toor4nsn', help='eNB ftp username.')
    parser_server_run.add_argument('--ftp_password', type=str, default='oZPS0POrRieRtu', help='eNB ftp password.')
    parser_server_run.add_argument('--definitions_file_path', type=str, default='', help='File path to InfoModel im.jar file.')
    parser_server_run.add_argument('--service_name', type=str, help='Service name.')
    parser_server_run.set_defaults(func=_run_infomodel_server)

    args = parser.parse_args()
    args.func(args)
