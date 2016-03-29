# -*- coding: utf-8 -*-
"""
:copyright: NSN
:author: Bartłomiej Idzikowski
:contact: bartlomiej.idzikowski@nsn.com
"""

from pkg_resources import resource_filename
from ute_common_java_remote.remote import JavaRemote


class ute_fault(JavaRemote):

    ROBOT_LIBRARY_SCOPE = 'TEST SUITE'

    CLASSPATH = [
        resource_filename(__name__, 'java'),
        resource_filename(__name__, 'java/resource/jars/commons-io-2.4.jar'),
        resource_filename(__name__, 'java/resource/jars/commons-net-3.3.jar'),
        resource_filename(__name__, 'java/resource/jars/guava-15.0.jar'),
        resource_filename(__name__, 'java/resource/jars/IMLibrary-1.1.6-SNAPSHOT.jar'),
        resource_filename(__name__, 'java/resource/jars/log4j-1.2.17.jar'),
        resource_filename(__name__, 'java/resource/jars/protobuf.jar'),
        resource_filename(__name__, 'java/resource/jars/slf4j-api-1.7.5.jar'),
        resource_filename(__name__, 'java/resource/jars/slf4j-log4j12-1.7.5.jar'),
        resource_filename(__name__, 'java/resource/jars/'),
    ]

    KEYWORD_CLASSES = ['ute_fault.FaultTrigger']

    def __init__(self):
        JavaRemote.__init__(self, ute_fault.CLASSPATH, ute_fault.KEYWORD_CLASSES)
