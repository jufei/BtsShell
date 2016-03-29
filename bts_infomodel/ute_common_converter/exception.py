# -*- coding: utf-8 -*-
"""Module to store all exceptions for converter package.

:author: Pawel Chomicki
:contact: pawel.chomicki@nsn.com
"""
from ute_core.exception import CoreException


class ConverterException(CoreException):
    """Base exception for converters."""


class ConvertError(ConverterException):
    """Exception raised when it is not possible to convert provided value."""
