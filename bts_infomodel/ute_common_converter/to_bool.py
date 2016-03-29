# -*- coding: utf-8 -*-
"""Module contains converters to bool type.

:author: Pawel Chomicki
:contact: pawel.chomicki@nsn.com
"""
from .base import BaseConverter
from .exception import ConvertError


class ToBool(BaseConverter):
    """Class tries to convert value to bool type.

    .. code-block:: python

        ToBool().convert("true")                    # Returns True
        ToBool(skip_none=True).convert("true")      # Returns True
        ToBool(skip_none=True).convert(None)        # Returns None
    """
    def __init__(self, skip_none=False):
        """
        :param boolean skip_none: Skip convert if the value is None.
        """
        self._skip_none = skip_none

    def convert(self, value):
        """Convert specified value to bool.

        :param value: Some value to convert.

        :return: Converted value.
        :rtype: boolean

        :raise: ConvertError if it is not possible to convert specified value.
        """
        if value is None and self._skip_none:
            return value
        if isinstance(value, basestring):
            return self._convert_to_bool(value)
        elif isinstance(value, bool):
            return value
        else:
            raise ConvertError('Object (%s) with value (%s) cannot be converted to bool' % (str(value), type(value).__name__))

    def _looks_like_false(self, value):
        if value.lower().strip() == "false":
            return True
        return False

    def _looks_like_true(self, value):
        if value.lower().strip() == "true":
            return True
        return False

    def _convert_to_bool(self, value):
        if self._looks_like_true(value):
            value = True
        elif self._looks_like_false(value):
            value = False
        else:
            raise ConvertError('Value is from out of range. Available values are (not case sensitive): ${True}, ${False}, true, false')
        return value


def to_bool(value, skip_none=False):
    """Method to made conversion to boolean.

    :param value: Some value to convert.
    :param boolean skip_none: Skip conversion if value is None.

    :return: Converted value.
    :rtype: boolean
    """
    return ToBool(skip_none=skip_none).convert(value)
