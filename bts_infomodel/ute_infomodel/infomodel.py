# -*- coding: utf-8 -*-
"""
:created on: 26-07-2013

:copyright: NSN
:author: Bartłomiej Idzikowski
:contact: bartlomiej.idzikowski@nsn.com
"""


import os
import sys
import subprocess
import collections
import Pyro4

sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'resource'))


from .decorator import exception_handler
from .util import logger as _logger, find_name_server, find_service, ProcessControl, turn_on_echo
from .nameserver import NameServerManager


class QueryResult(object):
    def __init__(self, result, query_data_timestamp, query_end_timestamp):
        """"QueryResult
        :param object result: Result of query
        :param float query_data_timestamp: query_data_timestamp
        :param float query_end_timestamp: query_end_timestamp
        """
        self.result = result
        self.query_data_timestamp = query_data_timestamp
        self.query_end_timestamp = query_end_timestamp

    def __str__(self):
        return str(self.result)


class InfoModelObject(dict):
    """InfoModel data object."""

    def __init__(self, dist_name, data):
        """
        :param string dist_name: Location of InfoModel object.
        :param dictionary data: InfoModel object data
        """
        self.dist_name = dist_name
        self.data = data
        for name, value in self.data.iteritems():
            new_dist_name = "{}.{}".format(dist_name, name)
            self[name] = self._wrap(value, new_dist_name)

    def _wrap(self, value, name):
        return InfoModelObject(name, value) if isinstance(value, dict) else value

    def __getattr__(self, attr):
        return self[attr]

    def __setattr__(self, attr, value):
        self[attr] = value

    def __str__(self):
        return self._dict_to_string(self.data, self.dist_name)

    def __len__(self):
        return len(self.data)

    def _dict_to_string(self, dump_dict, dist_name):
        """Change python dict to string in appropriate format.

        :param dictionary dump_dict: Dict, which was created from dump_object.
        :param string dist_name: Location of InfoModel object which we want to get.
        """
        result_string = ""
        for key, value in dump_dict.items():
            if isinstance(value, dict):
                result_string += self._dict_to_string(value, "{}.{}".format(dist_name, key))
            else:
                result_string += '{}.{} = {}\n'.format(dist_name, key, value)

        return result_string


class InfoModel(object):

    def __init__(self,
                 address=None,
                 port=None,
                 update_interval=None,
                 auto_reconnect=None,
                 definitions_file_path=None,
                 ftp_port=None,
                 ftp_username=None,
                 ftp_password=None,
                 name_server_manager=None,
                 ):
        """Constructor.

        :param string address: ENB ip address. Default: 192.168.255.1
        :param integer port: ENB info model port. Default: 15003.
        :param integer update_interval: The minimum updates interval[ms]. 0 means instant update. Default: 0.
        :param boolean auto_reconnect: Indicates whether we want to attempt automatic reconnection, when connection fails. Default: True.
        :param string definitions_file_path: Path to info model object definition file: im.jar
        """

        self.definitions_file_path = os.path.normpath(definitions_file_path) if definitions_file_path else ''
        self.address = address if address else '192.168.255.1'
        self.port = port if port else 15003
        self.update_interval = update_interval if update_interval else 0
        self.auto_reconnect = auto_reconnect if auto_reconnect is not None else True
        self.ftp_port = ftp_port if ftp_port is not None else 21
        self.ftp_username = ftp_username if ftp_username is not None else 'toor4nsn'
        self.ftp_password = ftp_password if ftp_password is not None else 'oZPS0POrRieRtu'

        self.min_heap_size = 'Xss1152k'
        self.max_heap_size = 'Xmx700m'

        self.package_dir = os.path.dirname(os.path.realpath(__file__))
        resource_dir = os.path.join(self.package_dir, "resource")
        infomodel_server_dir = os.path.join(resource_dir, "infomodel_server")
        infomodel_server_resource_dir = os.path.join(infomodel_server_dir, "resource")
        jars_dir = os.path.join(infomodel_server_resource_dir, "jars")
        jython_jar_path = os.path.join(os.environ.get('JYTHON_HOME', '/opt/ute/jython/2.7-b1'), "jython.jar")

        classpath = []
        for dirpath, dirnames, filenames in os.walk(jars_dir):
            classpath.extend([os.path.normpath(os.path.join(dirpath, filename)) for filename in filenames])

        classpath.extend([
            self.definitions_file_path,
            jython_jar_path,
            self.package_dir,
            infomodel_server_dir,
            resource_dir,
            os.path.normpath(jars_dir)
        ])

        self.classpath = os.pathsep.join(classpath)
        os.environ['CLASSPATH'], os.environ['JYTHONPATH'] = self.classpath, self.classpath
        self.infomodel_server_path = os.path.join(infomodel_server_dir, "server_cli.py")
        self.im_server_process = None
        self.infomodel_server = None
        self.name_server_manager = name_server_manager

    @exception_handler
    def connect(self, timeout, *args, **kw):
        """Connect to InfoModel."""
        return self.infomodel_server.start(timeout)

    @exception_handler
    def disconnect(self):
        """Disconnect from InfoModel."""
        return self.infomodel_server.stop()

    def _run_infomodel_server(self, service_name):
        args = [
            'java',
            '-%s' % self.max_heap_size,
            '-%s' % self.min_heap_size,
            '-XX:MaxPermSize=128M',
            '-Dpython.verbose=warning',
            '-classpath', self.classpath,
            'org.python.util.jython',
            self.infomodel_server_path, 'run',
            '--definitions_file_path', self.definitions_file_path,
            '--address', self.address,
            '--port', str(self.port),
            '--update_interval', str(self.update_interval),
            '--ftp_port', str(self.ftp_port),
            '--ftp_username', self.ftp_username,
            '--ftp_password', self.ftp_password,
            '--service_name', service_name,
        ]

        if self.auto_reconnect:
            args.append('--auto_reconnect')

        self.im_server_process = subprocess.Popen(args)

    def _configure_infomodel_server_connection(self, service_name):
        self.name_server = find_name_server()
        service_uri = find_service(self.name_server, service_name)
        self.infomodel_server = Pyro4.Proxy(service_uri)

    @exception_handler
    def setup(self, alias):
        """Setup InfoModel."""
        self.service_name = "%s_infomodel_server" % alias
        if self.name_server_manager is None:
            self.name_server_manager = NameServerManager(self.package_dir)
            self.name_server_manager.start()
        self._run_infomodel_server(self.service_name)
        self._configure_infomodel_server_connection(self.service_name)

    @exception_handler
    def teardown(self, is_basic_instance):
        """Teardown InfoModel. Release used resources."""
        try:
            self.infomodel_server.stop()
            self.infomodel_server.exit()
        except Pyro4.errors.ConnectionClosedError:
            _logger.error('Infomodel not connected.')
        finally:
            self.name_server.remove(self.service_name)
            ProcessControl(self.im_server_process).stop_process()
            # if is_basic_instance:
            #     self.name_server_manager.stop()
            #     turn_on_echo()

    @exception_handler
    def start_logger(self):
        """Start InfoModel logger."""
        return self.infomodel_server.start_logger()

    @exception_handler
    def stop_logger(self):
        """Stop InfoModel logger."""
        return self.infomodel_server.stop_logger()

    @exception_handler
    def save_log(self, filename, format):
        """Save InfoModel log."""
        return self.infomodel_server.save_log(filename, format)

    @exception_handler
    def clean_log(self):
        """Clean InfoModel log."""
        return self.infomodel_server.clean_log()

    @exception_handler
    def execute_operation(self, dist_name, operation, timeout=None, *args, **kw):
        """Execute operation on InfoModel object.

        :param string dist_name: Location InfoModel object inside InfoModel tree hierarchy.
        :param string operation: Name of operation to execute on InfoModel object.
        :param integer timeout: time in seconds after which attempt to execute operation will fail.

        :rtype: boolean
        """
        return self.infomodel_server.execute_operation(dist_name, operation, timeout, *args, **kw)

    @exception_handler
    def get_infomodel_object(self, dist_name, timeout=None):
        """Get InfoModel object.

        :param string dist_name: Location of InfoModel object.
        :param float timeout: Time in seconds after which getting dump object will fail.

        :rtype: InfoModelObject
        """
        return InfoModelObject(dist_name, self.infomodel_server.get_infomodel_object(dist_name, timeout))

    @exception_handler
    def query_infomodel(self, query, api_version=None, extend_result=None, timeout=None):
        """Query InfoModel.

        :param string query: query to be executed on InfoModel.
        :param string api_version: Version of query api.
        :param boolean extend_result: Extend query result with additional data like query data timestamp.
        :param float timeout: Time in seconds after which query operation will throw an error.

        :rtype: object
        """
        query_result = self.infomodel_server.execute_query(query, api_version, timeout)
        if isinstance(query_result, tuple):
            result, start_time, end_time = query_result
            if isinstance(result, dict):
                return QueryResult(InfoModelObject('', result), start_time, end_time) if extend_result else InfoModelObject('', result)
            elif isinstance(result, collections.Iterable):
                if extend_result:
                    return [QueryResult(InfoModelObject(*r), start_time, end_time) for r in result]
                else:
                    return [InfoModelObject(*r) for r in result]
            else:
                return QueryResult(result, start_time, end_time) if extend_result else result
        else:
            return query_result

    @exception_handler
    def query_infomodel_sequence(self, queries, api_version=None, timeout=None):
        """Query InfoModel.

        :param dictionary queries: queries to be executed on InfoModel.
        :param string api_version: Version of query api.
        :param float timeout: Time in seconds after which query operation will throw an error.

        :rtype: boolean
        """
        return self.infomodel_server.execute_query_sequence(queries, api_version, timeout)

    @exception_handler
    def query_infomodel_pararellel(self, queries, api_version=None, timeout=None):
        """Query InfoModel pararellel.

        :param dictionary queries: queries to be executed on InfoModel.
        :param string api_version: Version of query api.
        :param float timeout: Time in seconds after which query operation will throw an error.

        :rtype: boolean
        """
        return self.infomodel_server.execute_query_pararellel(queries, api_version, timeout)

    @exception_handler
    def query_infomodel_pararellel_sequences(self, sequences, api_version=None, timeout=None):
        """Query InfoModel pararellel sequences.

        :param dictionary sequences: sequences to be executed in pararellel.
        :param string api_version: Version of query api.
        :param float timeout: Time in seconds after which query operation will throw an error.

        :rtype: boolean
        """
        return self.infomodel_server.execute_query_pararellel_sequences(sequences, api_version, timeout)
