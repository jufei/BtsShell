# -*- coding: utf-8 -*-
"""
:created on: 12-12-2013

:copyright: NSN
:author: Bartłomiej Idzikowski
:contact: bartlomiej.idzikowski@nsn.com
"""


import random
from infomodel.dump import DistName, Operation, DumpObject
from com.nsn.oam.infomodel.communication.network import OperationExecutor
from com.nsn.oam.infomodel import ClassMapContainer
from infomodel_server.exception import \
    InfoModelObjectNotFoundException,\
    InfoModelOperationException,\
    InfoModelOperationNotFoundException,\
    InfoModelOperationParameterNotFoundException,\
    InfoModelOperationParameterWrongTypeException


class OperationModel(object):
    def __init__(self, model):
        self.model = model
        self.executor = OperationExecutor()

    def _check_operation_exists(self, type_info, operation):
        if type_info is None:
            raise InfoModelOperationNotFoundException('InfoModel operation: %s is not found.' % operation)

    def _check_operation_parameters(self, type_info, operation, **kw):
            if type_info.isComplex():
                for param in kw:
                    if param not in type_info.getComplexFields().keySet():
                        raise InfoModelOperationParameterNotFoundException('InfoModel operation: %s parameter: %s is not found.' % (operation, param))

    def _normalize_operation_name(self, operation):
        return operation if operation.startswith('Oper') or operation.startswith('oper_') else "Oper%s" % operation

    def _create_operation_object(self, operation):
        return Operation(DumpObject().getClass(), DumpObject(), operation)

    def _generate_request_id(self):
        return random.randint(0, 100000)

    def execute_operation(self, dist_name, operation, timeout, *args, **kw):
        """Execute InfoModel operation.

        :param string dist_name: Path to InfoModel object.
        :param string operation: Operation name.
        :param float timeout: Operation timeout in seconds.

        :return: Operation request id.
        """
        try:
            dist_name_obj = DistName.create(dist_name)
            managed_object_info = ClassMapContainer.managedObjectsInfo.getDefinition(dist_name_obj.getClassName())
            operation = self._normalize_operation_name(operation)
            type_info = managed_object_info.getOperations().get(operation)
            self._check_operation_exists(type_info, operation)
            self._check_operation_parameters(type_info, operation, **kw)
            dump_object = self.model.get_dump_object(dist_name_obj.distName, timeout)
            operation_obj = self._create_operation_object(operation)
            request_id = self._generate_request_id()
            message_builder = self.model.provider.getMessageBuilder()
            self.executor.execute(dist_name_obj, dump_object, operation_obj, kw, self.model.provider, message_builder, request_id)
            return request_id
        except InfoModelObjectNotFoundException, e:
            raise InfoModelOperationException(str(e))
