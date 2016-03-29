# -*- coding: utf-8 -*-
"""
:created on: 05-12-2013

:copyright: NSN
:author: Bartłomiej Idzikowski
:contact: bartlomiej.idzikowski@nsn.com
"""


from time import time
from java.net import InetAddress
from java.io import File
from infomodel.dump import DistName
from com.nsn.oam.infomodel.communication.network import ObjectDefinitionsFactory
from com.nsn.oam.infomodel.communication.network2 import NetworkDataProvider2
from com.nsn.oam.infomodel import ClassMapContainer
from com.nsn.oam.infomodel.common.utils.ftp import FtpProperties
from infomodel_server.exception import \
    InfoModelTimeoutException, \
    InfoModelConnectionException, \
    InfoModelObjectNotFoundException, \
    InfoModelObjectsNotFoundException
from .manager import ConnectionManager, ModelChangeManager
from .monitor import ConnectionStatusChangeMonitor, ModelChangeMonitor
from .util import dump_object_to_dict, logger
from .manager import ConnectionStatus


class IMModel(object):

    def __init__(self, address, port, update_interval, auto_reconnect, definitions_file_path, ftp_port, ftp_username, ftp_password):
        builder = NetworkDataProvider2.forAddress(InetAddress.getByName(address))\
            .withInfoModelPort(port)\
            .connectToRealBts()\
            .reconnectAutomatically(auto_reconnect)\
            .updateIntervalMs(update_interval)

        if definitions_file_path:
            object_definitions = ObjectDefinitionsFactory.getObjectDefinitions(File(definitions_file_path))
        else:
            ftp_properties = FtpProperties(address, ftp_port, ftp_username, ftp_password)
            object_definitions = ObjectDefinitionsFactory.getDefinitionsFromFtp(ftp_properties)

        builder.objectDefinitions(object_definitions)
        self.provider = builder.build()

        self.connection_manager = ConnectionManager()
        self.change_manager = ModelChangeManager()
        self.connection_status_monitor = ConnectionStatusChangeMonitor()
        self.model_change_monitor = ModelChangeMonitor()
        self.connection_status_monitor.register(self.connection_manager)
        self.model_change_monitor.register(self.change_manager)
        self.provider.registerForConnectionStatus(self.connection_status_monitor)
        self.provider.registerListener(self.model_change_monitor)

    def start(self, timeout):
        """Start InfoModel data provider."""
        self.provider.run()

    def stop(self):
        """Stop InfoModel data provider."""
        self.provider.stop()

    def get_dump_objects_map(self, timeout):
        """Get InfoModel DumpObject's."""
        try:
            self.change_manager.wait_for_any_action(timeout)
            return self.provider.getDump().getObjects()
        except InfoModelTimeoutException:
            raise InfoModelObjectsNotFoundException('InfoModel objects not found.')

    def get_dump_object(self, dist_name, timeout):
        """Returns dump object from location pointed by dist_name."""
        try:
            dump_object = None
            start_time = time()
            dist_name_object = DistName.create(dist_name)
            while dump_object is None and time() - start_time <= timeout:
                dump_object = self.provider.getDump().objects.get(dist_name_object)
                if dump_object is None:
                    self.change_manager.wait_for_any_action(timeout - (time() - start_time))

            if dump_object:
                return dump_object
            raise InfoModelObjectNotFoundException('InfoModel object not found.')
        except InfoModelTimeoutException:
            raise InfoModelObjectNotFoundException('InfoModel object not found.')

    def get_infomodel_object(self, dist_name, timeout):
        """Get InfoModel object as dict."""
        dump_object = self.get_dump_object(dist_name, timeout)
        return dump_object_to_dict(dump_object)
