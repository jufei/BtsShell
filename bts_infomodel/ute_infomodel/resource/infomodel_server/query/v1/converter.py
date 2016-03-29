# -*- coding: utf-8 -*-
"""
:created on: 03-12-2013

:copyright: NSN
:author: Tomasz Kolek
:contact: tomasz.kolek@nsn.com
"""

from abc import ABCMeta, abstractmethod


class ToBool(object):
    """Class tries to convert value to bool type"""
    def __init__(self, skip_none=False):
        """
        :param boolean skip_none: Skip convert if the value is None
        """
        self._skip_none = skip_none

    def convert(self, value):
        """Convert specified value to bool

        :param value: Some value to convert

        :return: Converted value
        :rtype: boolean

        :raise: ConvertError if it is not possible to convert specified value
        """
        if value is None and self._skip_none:
            return value
        if isinstance(value, basestring):
            return self._convert_to_bool(value)
        elif isinstance(value, bool):
            return value
        else:
            raise Exception('Object (%s) with value (%s) cannot be converted to bool' % (str(value), type(value).__name__))

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
            raise Exception('Value is from out of range. Available values are (not case sensitive): ${True}, ${False}, true, false')
        return value


def to_bool(value, skip_none=False):
    """Method to made conversion to boolean

    :param value: Some value to convert
    :param boolean skip_none: Skip conversion if value is None

    :return: Converted value
    :rtype: boolean
    """
    return ToBool(skip_none=skip_none).convert(value)


class ToInt(object):
    """Class tries to convert value to int type"""
    def __init__(self, skip_none=False):
        """
        :param boolean skip_none: Skip convert if the value is None
        """
        self._skip_none = skip_none

    def convert(self, value):
        """Method to convert specified value to int

        :param value: Value to convert

        :return: Converted value
        :rtype: integer

        :raise: ConvertError if it is not possible to convert specified value
        """
        if value is None and self._skip_none:
            return value
        try:
            return int(value)
        except (ValueError, TypeError):
            raise Exception('Value (%s) is not a number e.g. 1, ${1}' % str(value))


def to_int(value, skip_none=False):
    """Method to made conversion to integer

    :param value: Some value to convert
    :param boolean skip_none: Skip conversion if value is None

    :return: Converted value
    :rtype: integer
    """
    return ToInt(skip_none=skip_none).convert(value)


def to_float(value, skip_none=False):
    """to_float"""
    if value is None and skip_none is True:
        return value
    if isinstance(value, basestring) or isinstance(value, int):
        try:
            return float(value)
        except ValueError:
            raise ValueError('Value (%s) is not a floating point number representation' % str(value))
    elif isinstance(value, float):
        return value
    else:
        raise TypeError('Object (%s) with value (%s) cannot be converted to float' % (str(value), type(value).__name__))


def convert_type(value):
    """convert value to one of the types [bool, int, float, str]"""
    converters = [to_bool, to_int, to_float, str]
    for converter in converters:
        try:
            return converter(value)
        except:
            pass
    return Exception('Can not convert type of: %s' % value)


class Converter(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def convert(self, value):
        """Base converter"""


class DistNameToRegexpConverter(Converter):

    def convert(self, value):
        """convert distname to regex expression"""
        regexp_start = '' if value.startswith('//') else '^'
        regexp_body = value.replace('*', '([1-9][0-9]*)').replace('//', '.*/')
        regexp_end = '$'
        return regexp_start + regexp_body + regexp_end


class InfoModelConverter(Converter):

    def _get_function(self, parsed_query):
        return getattr(parsed_query, 'function', 'check')

    def _get_dist_name(self, parsed_query):
        return parsed_query.dist_name

    def _get_predicates(self, parsed_query):
        predicates_list = parsed_query.predicates
        return tuple([(predicate.name, predicate.symbol, convert_type(predicate.value)) for predicate in predicates_list])

    def _get_condition(self, parsed_query):
        return parsed_query.condition.symbol, int(parsed_query.condition.value)

    def convert(self, parsed_query):
        """convert"""
        result_dict = dict()
        result_dict['function'] = self._get_function(parsed_query)
        result_dict['dist_name'] = DistNameToRegexpConverter().convert(self._get_dist_name(parsed_query))
        result_dict['predicates'] = self._get_predicates(parsed_query)
        if result_dict['function'] == 'count':
            result_dict['condition_symbol'], result_dict['condition_value'] = self._get_condition(parsed_query)

        return result_dict
