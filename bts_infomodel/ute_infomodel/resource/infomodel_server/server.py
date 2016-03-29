# -*- coding: utf-8 -*-
"""
:created on: 30-07-2013

:copyright: NSN
:author: Bartłomiej Idzikowski
:contact: bartlomiej.idzikowski@nsn.com
"""


from .util import logger as _logger
from .decorator import exception_handler, check_connection_status
from .query.factory import QueryExecutorFactory
from .model import IMModel
from .operation.model import OperationModel
from .logger.model import LoggerModel
from .manager import ConnectionStatus
import threading


class InfoModelServer(object):

    def __init__(self, address, port, update_interval, auto_reconnect, definitions_file_path, ftp_port, ftp_username, ftp_password):
        self._is_running = True
        self.model = IMModel(address, port, update_interval, auto_reconnect, definitions_file_path, ftp_port, ftp_username, ftp_password)
        self.logger_model = LoggerModel(self.model)

    @exception_handler
    def start_logger(self):
        """Start logger."""
        self.logger_model.start()

    @exception_handler
    def stop_logger(self):
        """Stop logger."""
        self.logger_model.stop()

    @exception_handler
    def save_log(self, filename, log_format):
        """Save InfoModel logger data.

        :param string filename: Path to log.
        :param string log_format: Log format currently only `ims`.
        """
        self.logger_model.save(filename, log_format)

    @exception_handler
    def clean_log(self):
        """Clean logger data."""
        self.logger_model.clean()

    @exception_handler
    @check_connection_status
    def execute_operation(self, dist_name, operation, timeout, *args, **kw):
        """Execute operation on InfoModel object.

        :param string dist_name: Location inside InfoModel tree hierarchy.
        :param string operation: Name of operation to execute on InfoModel node.
        :param float timeout: Time in seconds after which attempt to execute operation will fail.
        """
        return OperationModel(self.model).execute_operation(dist_name, operation, timeout, *args, **kw)

    @exception_handler
    @check_connection_status
    def get_infomodel_object(self, dist_name, timeout):
        """Get information InfoModel object, which you gave as dist_name."""
        return self.model.get_infomodel_object(dist_name, timeout)

    @exception_handler
    @check_connection_status
    def execute_query(self, query, api_version, timeout):
        """Execute infomodel query."""
        return QueryExecutorFactory(api_version, self.model).execute(query, timeout)

    @exception_handler
    @check_connection_status
    def execute_query_sequence(self, queries, api_version, timeout):
        """Execute infomodel query sequence."""
        return QueryExecutorFactory(api_version, self.model).execute_sequence(queries, timeout)

    @exception_handler
    @check_connection_status
    def execute_query_pararellel(self, queries, api_version, timeout):
        """Execute infomodel query pararellel."""
        return QueryExecutorFactory(api_version, self.model).execute_pararellel(queries, timeout)

    @exception_handler
    @check_connection_status
    def execute_query_pararellel_sequences(self, sequences, api_version, timeout):
        """Execute infomodel query pararellel sequences."""
        return QueryExecutorFactory(api_version, self.model).execute_pararellel_sequences(sequences, timeout)

    @exception_handler
    def start(self, timeout):
        """Run infomodel provider."""
        self.model.start(timeout)
        self.model.connection_manager.wait_for_status(ConnectionStatus.REGISTERED_TO_INFOMODEL, timeout)

    @exception_handler
    def stop(self):
        """Stop infomodel provider."""
        self.model.stop()

    @exception_handler
    def exit(self):
        """Exit from infomodel server."""
        self._is_running = False
        # _logger.error('Server exit. Quiting...')  #Comment by Jufei

    def is_running(self):
        """Check if server is running."""
        return self._is_running
