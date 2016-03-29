# -*- coding: utf-8 -*-
"""Module contains converters to list of specified types.

:author: Pawel Chomicki
:contact: pawel.chomicki@nsn.com
"""
from .base import BaseConverter
from .exception import ConvertError


class ToTypeList(BaseConverter):
    """Class tries to convert current list to list of specified type.

    .. code-block:: python

        ToTypeList(convert_method=int).convert(["1", "2"])                      # Returns [1, 2]
        ToTypeList(convert_method=int, skip_none=True).convert(["1", "2"])      # Returns [1, 2]
        ToTypeList(convert_method=int, skip_none=True).convert(None)            # Returns None
    """
    def __init__(self, convert_method, skip_none=False):
        """
        :param convert_method: Method needed to convert value e.g. str, bool, int.
        :param boolean skip_none: Skip convert if the value is None.
        """
        self._expected_type = convert_method
        self._skip_none = skip_none

    def convert(self, current_list):
        """Method to convert current list to list of specified type.

        :param list current_list: List to convert.
        :return: Converted list
        :rtype: list

        :raise: ConvertError if it is not possible to convert any value of the specified list.
        """
        if current_list is None and self._skip_none is True:
            return current_list
        new_list = []
        for index, each in enumerate(current_list):
            try:
                new_list.append(self._expected_type(each))
            except ValueError:
                raise ConvertError('Value (%s) with index (%d) cannot be converted to (%s)' % (str(each), index, self._expected_type.__name__))
        return new_list


def to_type_list(rlist, convert_method, skip_none=False):
    """Method to made conversion to list of specified type.

    :param list rlist: List to convert.
    :param convert_method: Method needed to convert value e.g. str, bool, int.
    :param boolean skip_none: Skip conversion if provided rlist object is None.

    :return: Converted list.
    :rtype: list
    """
    return ToTypeList(convert_method=convert_method, skip_none=skip_none).convert(rlist)


def to_int_list(rlist, skip_none=False):
    """Method to made conversion to list of integers.

    :param list rlist: List to convert.
    :param boolean skip_none: Skip conversion if provided rlist object is None.

    :return: Converted list.
    :rtype: list
    """
    return ToTypeList(convert_method=int, skip_none=skip_none).convert(rlist)
