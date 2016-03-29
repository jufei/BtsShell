"""bts infomodel is inherited from ute_infomodel to keep the interface unfied
in TA team"""
import sys
import os
from time import sleep

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from ute_infomodel import ute_infomodel

__version__ = "1.18.2"

class bts_infomodel(ute_infomodel):
    ROBOT_LIBRARY_SCOPE = "TEST SUITE"
    ROBOT_LIBRARY_VERSION = __version__

    def __init__(self):
        super(bts_infomodel, self).__init__()

    def connect_infomodel(self, timeout=10, *args, **kw):
        """Connect to infomodel."""
        try:
            result = super(bts_infomodel, self).connect_infomodel(timeout=timeout, *args, **kw)
        except Exception, e:
            print "*WARN* ", e
            sleep(5)
            result = super(bts_infomodel, self).connect_infomodel(timeout=timeout, *args, **kw)
        return result

    def disconnect_infomodel(self, timeout=10, *args, **kw):
        """Disconnect from infomodel."""
        return super(bts_infomodel, self).disconnect_infomodel(timeout=timeout, *args, **kw)

    def setup_infomodel(self, address='192.168.255.1', port=15003, update_interval=0, auto_reconnect=True, definitions_file_path=None, *args, **kw):
        """
        :param string im_jar_path: Path to info model object definition file: im.jar.
        :param string address: BTS ip address.
        :param integer port: BTS infomodel port. Default: 15003.
        :param integer update_interval: The minimum updates interval[ms]. 0 means instant update. Default: 0.
        :param boolean target_connection: Indicates whether it is connection to the real BTS. Default: True
        :param boolean auto_reconnect: Indicates whether we want to attempt automatic reconnection, when connection fails. Default: True.
        """
        if sys.platform == 'win32':
           kill_cmd = """wmic process where "commandline like '%java%%ute_infomodel%' or commandline like '%python%nameserver.py%'" delete"""
        else:
           kill_cmd = 'ps ax | grep -E "(java.*ute_infomodel|python.*nameserver.py)" | awk \'{print $1}\' | xargs kil        print "set up infomodel with follow info: ", definitions_file_path, address, port'

        if "default" in self.store.aliases:
            self.store.remove("default")
        try:
            result = super(bts_infomodel, self).setup_infomodel(address=address, port=port,
                                                                update_interval=update_interval,
                                                          auto_reconnect=auto_reconnect,
                                                          definitions_file_path=definitions_file_path,
                                                           *args, **kw)
        except Exception, e:
            print "*WARN* ", e
            sleep(5)
            if "default" in self.store.aliases:
                self.store.remove("default")
            result = super(bts_infomodel, self).setup_infomodel(address=address, port=port,
                                                                update_interval=update_interval,
                                                          auto_reconnect=auto_reconnect,
                                                          definitions_file_path=definitions_file_path,
                                                           *args, **kw)
        return result

    def teardown_infomodel(self, *args, **kw):
        """Teardown InfoModel"""
        return super(bts_infomodel, self).teardown_infomodel(*args, **kw)

    def start_infomodel_logger(self, *args, **kw):
        """Start infomdoel logger."""
        return super(bts_infomodel, self).start_infomodel_logger(*args, **kw)

    def stop_infomodel_logger(self, *args, **kw):
        """Stop infomodel logger."""
        return super(bts_infomodel, self).stop_infomodel_logger(*args, **kw)

    def save_infomodel_log(self, filename, format='ims2', *args, **kw):
        """Dump infomodel logger.

        :param String filename: Dump filename or path to dumpfile
        :param String format: Dump file format. Default: ims
        """
        return super(bts_infomodel, self).save_infomodel_log(filename, format=format, *args, **kw)

    def clean_infomodel_log(self, *args, **kw):
        """Clean infomodel logger."""
        return super(bts_infomodel, self).clean_infomodel_log(*args, **kw)


    def execute_infomodel_operation(self, dist_name, operation, timeout=10, *args, **kw):
        """Execute operation on infomodel node

        :param string dist_name: Location inside infomodel tree hierarchy
        :param string operation: operation name to execute on infomodel node
        :param dict operation_parameters: dictionary of parameters to be passed to operation
        :param int timeout: time in seconds after which attempt to execute operation will fail

        :rtype: bool

        :note: Every leaf node of infomodel has its own operation set.
        :note: Infomodel location should be given without slash at the end.
        """
        return super(bts_infomodel, self).execute_infomodel_operation(dist_name, operation, timeout=timeout, *args, **kw)

    def get_infomodel_object(self, dist_name, timeout=10, *args, **kw):
        """Enable infomodel diagnostic

        :param InfoModel im: InfoModel object
        :param string dist_name: Location of infomodel object
        :param float timeout: Time in seconds after which getting dump object will fail
        """
        return super(bts_infomodel, self).get_infomodel_object(dist_name, timeout=timeout, *args, **kw)

    def query_infomodel(self, query, api_version='v1', timeout=10, *args, **kw):
        """Query infomodel

        :param string query: Location of infomodel object
        :param float timeout: Time in seconds after query operation will throw InfoModelTimeOutException
        :param string executor: default python executor
        """
        return super(bts_infomodel, self).query_infomodel(query, api_version=api_version, timeout=timeout, *args, **kw)

    def query_infomodel_sequence(self, api_version='v1', timeout=10, alias='default', **kw):
        """Query infomodel

        :param string query: Location of infomodel object
        :param float timeout: Time in seconds after query operation will throw InfoModelTimeOutException
        :param string executor: default python executor
        """
        return super(bts_infomodel, self).query_infomodel_sequence(api_version=api_version,
                                                                   timeout=timeout,
                                                                   alias='default', **kw)
