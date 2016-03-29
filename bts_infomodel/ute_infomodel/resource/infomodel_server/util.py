# -*- coding: utf-8 -*-
"""
:created on: 03-12-2013

:copyright: NSN
:author: Tomasz Kolek
:contact: tomasz.kolek@nsn.com
"""

from java.util import ArrayList
import logging
from time import time, sleep
import Pyro4

from infomodel.dump import DumpObject

logger = logging.getLogger(__file__)
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)


def find_name_server(timeout=180):
    """Locate Pyro4 name server."""
    stime = time()
    name_server = None
    while not name_server and time() - stime <= timeout:
        try:
            name_server = Pyro4.naming.locateNS()
        except:
            logger.debug('Finding Pyro4 name server from server.')
            sleep(1)
    return name_server


def convert_list_objects(objects_list, objects_types):
    """Convert Java ArrayList to python list"""
    converted_list = []
    if objects_list is not None:
        for v in objects_list:
            v_type = str(v.getType())[17:-2]
            if v.getType() == DumpObject:
                converted_list.append(dump_object_to_dict(v.getValue()) if v.getValue() is not None else None)
            elif v_type in objects_types:
                converted_list.append(v.getValue())
            else:
                converted_list.append(str(v.getValue()))
    return converted_list


def dump_object_to_dict(dump_object):
    """Change dump object to a python dict

    :param DumpObject dump_object: Dump object to convert.
    """
    param_types = ['double', 'str', 'int', 'float', 'None', 'long',
                   'java.lang.Integer', 'java.lang.Double', 'java.lang.Float', 'java.lang.Boolean', 'java.lang.Long']
    result_dict = {}
    for key in dump_object.parameters.keySet():
        param = dump_object.parameters.get(key)
        if param.getType() == DumpObject:
            result_dict[key] = dump_object_to_dict(param.getValue()) if param.getValue() is not None else None
        else:
            param_type = str(param.getType())[7:-2]
            if param_type in param_types:
                result_dict[key] = param.getValue()
            elif param.getType() == ArrayList:
                result_dict[key] = convert_list_objects(param.getValue(), param_types)
            else:
                result_dict[key] = str(param.getValue())
    return result_dict
