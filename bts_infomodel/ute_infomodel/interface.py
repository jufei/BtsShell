#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
:created on: 26-07-2013

:copyright: NSN
:author: Bartłomiej Idzikowski
:contact: bartlomiej.idzikowski@nsn.com
"""

from robot.utils.robottime import timestr_to_secs
from ute_common_converter.to_bool import to_bool
from ute_common_converter.to_number import to_int, to_float
from ute_common_store.store import Store
from ute_common_validator.validator import And, IsString, IsIpAddress, IsNumber, ValidLength, IsOneOf, InRange, IsInstance
from infomodel import InfoModel
from .exception import InfoModelMissingDefinitionsFilePathException


class ute_infomodel(object):

    ROBOT_LIBRARY_SCOPE = 'TEST SUITE'
    ROBOT_LISTENER_API_VERSION = 2

    def __init__(self):
        self.store = Store()
        self.ROBOT_LIBRARY_LISTENER = self

    def connect_infomodel(self, timeout=10, alias='default'):
        """Connect to InfoModel. Keyword will wait some `timeout` time for successful connection or throw error if connection fail.

        :param float timeout: Connection timeout.
        """
        timeout = timestr_to_secs(timeout)
        IsNumber().check(timeout)
        IsString().check(alias)
        self.store.get(alias).connect(timeout)

    def disconnect_infomodel(self, alias='default'):
        """Disconnect from InfoModel.

        :param string alias: Name of execution context.
        """
        IsString().check(alias)
        self.store.get(alias).disconnect()

    def setup_infomodel(self,
                        address='192.168.255.1',
                        port=12346,
                        update_interval=0,
                        auto_reconnect=True,
                        definitions_file_path=None,
                        ftp_port=21,
                        ftp_username='toor4nsn',
                        ftp_password='oZPS0POrRieRtu',
                        alias='default',
                        ):
        """Setup InfoModel library.

        :param string address: eNB ip address.
        :param integer port: eNB InfoModel port.
        :param integer update_interval: The minimum updates interval[ms]. 0 means instant update.
        :param boolean auto_reconnect: Indicates whether we want to attempt automatic reconnection, when connection fails.
        :param string definitions_file_path: Path to info model object definition file: im.jar, meta.zip.
               By default if path is not set, library will automatically download meta.zip from eNB.
        :param integer ftp_port: eNB ftp port.
        :param string ftp_username: eNB ftp username.
        :param string ftp_password: enB ftp password.
        :param string alias: Name of execution context.

        :note: Decoding messages with im.jar will be deprecated in the future.
        """
        port = to_int(port)
        update_interval = to_int(update_interval)
        auto_reconnect = to_bool(auto_reconnect)
        ftp_port = to_int(ftp_port)

        And(IsString(), IsIpAddress()).check(address)
        And(IsNumber(), IsInstance(int), IsOneOf(15001, 15002, 15003, 15004, 15005, 12345, 12346, 12347)).check(port)
        IsNumber().check(update_interval)
        IsInstance(bool).check(auto_reconnect)
        And(IsNumber(), IsInstance(int)).check(ftp_port)
        And(IsString(), ValidLength(1, 15)).check(ftp_username)
        And(IsString(), ValidLength(1, 15)).check(ftp_password)
        IsString().check(alias)

        infomodel = InfoModel(address,
                              port,
                              update_interval,
                              auto_reconnect,
                              definitions_file_path,
                              ftp_port,
                              ftp_username,
                              ftp_password,
                              self._get_name_server_manager())
        self.store.add(infomodel, alias)
        self.store.get(alias).setup(alias)

    def _get_name_server_manager(self):
        for stored_alias in self.store.aliases:
            name_server_manager = getattr(self.store.get(stored_alias), 'name_server_manager', None)
            if name_server_manager:
                return name_server_manager
        return None

    def teardown_infomodel(self, alias='default'):
        """Teardown InfoModel. Keyword will release used resources.

        :param string alias: Name of execution context.
        """
        IsString().check(alias)
        self.store.get(alias).teardown(len(self.store.aliases) == 1)
        self.store.remove(alias)

    def start_infomodel_logger(self, alias='default'):
        """Start InfoModel logger.

        :param string alias: Name of execution context.
        """
        IsString().check(alias)
        self.store.get(alias).start_logger()

    def stop_infomodel_logger(self, alias='default'):
        """Stop InfoModel logger.
        :param string alias: Name of execution context.
        """
        IsString().check(alias)
        self.store.get(alias).stop_logger()

    def save_infomodel_log(self, filename, format='ims2', alias='default'):
        """Save InfoModel log.

        :param string filename: Infomodel log filename or path to dumpfile
        :param string format: Infomodel log in .ims2 format. Support for .ims format was removed.
        :param string alias: Name of execution context.
        """
        IsString().check(filename)
        And(IsString(), IsOneOf('ims2')).check(format)
        IsString().check(alias)
        self.store.get(alias).save_log(filename, format)

    def clean_infomodel_log(self, alias='default'):
        """Clean InfoModel log.

        :param string alias: Name of execution context.
        """
        IsString().check(alias)
        self.store.get(alias).clean_log()

    def execute_infomodel_operation(self, dist_name, operation, timeout=10, alias='default', *args, **kw):
        """Execute operation on InfoModel object. Keyword will wait some `timeout` for successful operation result or throw error if.operation fail.

        :param string dist_name: Location of InfoModel object.
        :param string operation: Name of operation to execute on InfoModel object.
        :param float timeout: Time in seconds after which attempt to execute operation will fail.
        :param string alias: Name of execution context.
        """
        timeout = timestr_to_secs(timeout)
        IsString().check(dist_name)
        IsString().check(operation)
        IsNumber().check(timeout)
        IsString().check(alias)
        return self.store.get(alias).execute_operation(dist_name, operation, timeout, *args, **kw)

    def get_infomodel_object(self, dist_name, timeout=10, alias='default'):
        """Get InfoModel object from some `dist_name`. Keyword will wait some `timeout` for successful result or throw error.

        :param string dist_name: Location of InfoModel object.
        :param float timeout: Time in seconds after which getting InfoModel object will fail.
        :param string alias: Name of execution context.
        """
        timeout = timestr_to_secs(timeout)
        IsString().check(dist_name)
        IsNumber().check(timeout)
        IsString().check(alias)
        return self.store.get(alias).get_infomodel_object(dist_name, timeout=timeout)

    def query_infomodel(self, query, api_version='v1', timeout=10, alias='default', extend_result=False):
        """Query InfoModel with some `query`. Keyword will wait for successful result some `timeout` time or fail.

        :param string query: Query expression on InfoModel.

            # example values for `query` parameter:

            # Check that number of `D` objects under /A-1/B-1/C-1 path is more than 1.
            query=count /A-1/B-1/C-1/D-* is > 1

            # Check that number of `D` objects with parameter `ParameterName` equal to `Value` at /A-1/B-1/C-1 path is greater than 1.
            query=count /A-1/B-1/C-1/D-* is [ParameterName=Value] > 1

            # Check that D-1 object exists under /A-1/B-1/C-1 path.
            query=/A-1/B-1/C-1/D-1

            # Check that E-1 object exists under /A-1/B-1/C-1/D-1 path and has two parameters with specified values.
            query=/A-1/B-1/C-1/D-1/E-1 is [ParameterName1=Value1,ParameterName2=Value2]

            # Check that any E-* object exists under /A-1/B-1/C-1/D-1 path and have two parameters with specified values.
            query=/A-1/B-1/C-1/D-1/E-* is [ParameterName1=Value1,ParameterName2=Value2]

            # Check that every E object under /A-1/B-1/C-1/D-1 path have parameters with specified values.
            # At least one object has to match query.
            query=every /A-1/B-1/C-1/D-1/E-* is [ParameterName1=ParamValue1,ParameterName2=ParamValue2]

            # Check that any E object under /A-1/B-1/C-1/D-1 path have parameters with values matched with given regex.
            # At least one object has to match query.
            query=/A-1/B-1/C-1/D-1/E-* is [ParameterName1=regex"ParamValue1",ParameterName2=regex"ParamValue[0-9]"]

            # Check that E-1 object under /A-1/B-1/C-1/D-1 path have parameter, as list, with index 2 equals to "2 index"
            query=/A-1/B-1/C-1/D-1/E-1 is [ParameterName[2]="2 index"]

            # Check that E-1 object under /A-1/B-1/C-1/D-1 path have parameter, as list, where every element are equals to "2 index"
            query=/A-1/B-1/C-1/D-1/E-1 is [ParameterName[*]="2 index"]

            # Check that E-1 object under /A-1/B-1/C-1/D-1 path have parameter, as list, where any element are equals to "2 index"
            query=/A-1/B-1/C-1/D-1/E-1 is [ParameterName[?]="2 index"]

            # Get all E objects under /A-1/B-1/C-1/D-1 path have parameter with specified value"
            query=get list /A-1/B-1/C-1/D-1/E-* is [ParameterName="Value"]

            # Get count of objects which match /A-1/B-1/C-1/D-* is [parameter=value]
            query=get count /A-1/B-1/C-1/D-* is [parameter=value]

            # Check if exists /A-1/B-1 object with empty param Value (e.g. empty list, empty string)
            query=/A-1/B-1 is [Value=empty]

            # Check if exists /A-1/B-1 object with non empty param Value (e.g. list, string)
            query=/A-1/B-1 is [Value!=empty]

        :param string api_version: Query api version. Currently available api version is 'v1'.
        :param boolean extend_result: Extend result with additional data like query data timestamp.
        :param float timeout: Time in seconds after witch query operation will throw InfoModelQueryTimeoutException.
        :param string alias: Name of execution context.

        :rtype: object
        """
        timeout = timestr_to_secs(timeout)
        extend_result = to_bool(extend_result)
        IsString().check(query)
        And(IsString(), IsOneOf('v1')).check(api_version)
        IsNumber().check(timeout)
        IsString().check(alias)
        return self.store.get(alias).query_infomodel(query, api_version, extend_result, timeout)

    def query_infomodel_sequence(self, api_version='v1', timeout=10, alias='default', **kw):
        """Query infomodel sequence. Keyword will wait for successful result some `timeout` time or fail.

        :param string api_version: Query api version. Currently available api version is 'v1'.
        :param float timeout: Time in seconds after witch query operation will throw InfoModelQueryTimeoutException.
        :param string alias: Name of execution context.

        :note: Experimental keyword.
        """
        timeout = timestr_to_secs(timeout)
        And(IsString(), IsOneOf('v1')).check(api_version)
        IsNumber().check(timeout)
        IsString().check(alias)
        return self.store.get(alias).query_infomodel_sequence(queries=kw, api_version=api_version, timeout=timeout)

    def query_infomodel_pararellel(self, api_version='v1', timeout=10, alias='default', **kw):
        """Query infomodel pararellel. Keyword will wait for successful result some `timeout` time or fail.

        :param string api_version: Query api version. Currently available api version is 'v1'.
        :param float timeout: Time in seconds after witch query operation will throw InfoModelQueryTimeoutException.
        :param string alias: Name of execution context.

        :note: Experimental keyword.
        """
        timeout = timestr_to_secs(timeout)
        And(IsString(), IsOneOf('v1')).check(api_version)
        IsNumber().check(timeout)
        IsString().check(alias)
        return self.store.get(alias).query_infomodel_pararellel(queries=kw, api_version=api_version, timeout=timeout)

    def query_infomodel_pararellel_sequences(self, api_version='v1', timeout=10, alias='default', **kw):
        """Query infomodel pararellel sequences. Keyword will wait for successful result some `timeout` time or fail.

        :param string api_version: Query api version. Currently available api version is 'v1'.
        :param float timeout: Time in seconds after witch query sequence will throw InfoModelQueryTimeoutException.
        :param string alias: Name of execution context.

        :note: Experimental keyword.
        """
        timeout = timestr_to_secs(timeout)
        And(IsString(), IsOneOf('v1')).check(api_version)
        IsNumber().check(timeout)
        IsString().check(alias)
        return self.store.get(alias).query_infomodel_pararellel_sequences(sequences=kw, api_version=api_version, timeout=timeout)

    def create_query_sequence(self, **kw):
        """Create query sequence."""
        return kw

    def _end_suite(self, name, attrs):
        for alias in self.store.aliases:
            self.teardown_infomodel(alias)
