# -*- coding: utf-8 -*-
"""Module contains converters to int type.

:author: Pawel Chomicki
:contact: pawel.chomicki@nsn.com
"""
from .base import BaseConverter
from .exception import ConvertError


class ToInt(BaseConverter):
    """Class tries to convert value to int type.

    .. code-block:: python

        ToInt().convert("5")                    # Returns 5
        ToInt(skip_none=True).convert("10")     # Returns 10
        ToInt(skip_none=True).convert(None)     # Returns None
    """
    def __init__(self, skip_none=False):
        """
        :param boolean skip_none: Skip convert if the value is None.
        """
        self._skip_none = skip_none

    def convert(self, value):
        """Method to convert specified value to int.

        :param value: Value to convert.

        :return: Converted value.
        :rtype: integer

        :raise: ConvertError if it is not possible to convert specified value.
        """
        if value is None and self._skip_none:
            return value
        try:
            return int(value)
        except (ValueError, TypeError):
            raise ConvertError('Value (%s) is not a number e.g. 1, ${1}' % str(value))


def to_int(value, skip_none=False):
    """Method to made conversion to integer.

    :param value: Some value to convert.
    :param boolean skip_none: Skip conversion if value is None.

    :return: Converted value.
    :rtype: integer
    """
    return ToInt(skip_none=skip_none).convert(value)


class ToFloat(BaseConverter):
    """Class tries to convert value from basestring or integer to float.

    .. code-block:: python

        ToFloat().convert("2.2")                    # Returns 2.2
        ToFloat(skip_none=True).convert("2.2")      # Returns 2.2
        ToFloat(skip_none=True).convert(None)       # Returns None
    """
    def __init__(self, skip_none=False):
        """
        :param boolean skip_none: Skip convert if the value is None.
        """
        self._skip_none = skip_none

    def convert(self, value):
        """Method to convert provided value to float type

        :param value: Value to convert.

        :return: Converted value.
        :rtype: float
        """
        if value is None and self._skip_none is True:
            return value
        if isinstance(value, basestring) or isinstance(value, int):
            return self._convert_to_float(value)
        elif isinstance(value, float):
            return value
        else:
            raise ConvertError('Object (%s) with value (%s) cannot be converted to float' % (str(value), type(value).__name__))

    def _convert_to_float(self, value):
        try:
            return float(value)
        except ValueError:
            raise ConvertError('Value (%s) is not a floating point number representation' % str(value))


def to_float(value, skip_none=False):
    """Method to made conversion to float.

    :param value: Some value to convert.
    :param boolean skip_none: Skip conversion if value is None.

    :return: Converted value.
    :rtype: integer
    """
    return ToFloat(skip_none=skip_none).convert(value)
