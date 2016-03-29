# -*- coding: utf-8 -*-
"""
:created on: 07-11-2013

:copyright: NSN
:author: Bartłomiej Idzikowski
:contact: bartlomiej.idzikowski@nsn.com
"""


from ute_core.exception import CoreException


class InfoModelException(CoreException):
    """InfoModel base Exception"""


class InfoModelMissingDefinitionsFilePathException(InfoModelException):
    """InfoModelMissingDefinitionsFilePathException is raised when path to definitions file is not set."""


class InfoModelUnexpectedException(InfoModelException):
    """InfoModelUnexpectedException is raised when reason is unknown."""
