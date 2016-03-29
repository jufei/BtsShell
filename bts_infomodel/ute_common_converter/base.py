# -*- coding: utf-8 -*-
"""
:author: Pawel Chomicki
:contact: pawel.chomicki@nsn.com
"""
from abc import ABCMeta, abstractmethod


class BaseConverter(object):
    """Base class for all converters. Every converter has to implement convert method to have common way of executing conversion operation."""
    __metaclass__ = ABCMeta

    @abstractmethod
    def convert(self, value, *args, **kwargs):
        """Method makes conversion from specified value to specified type."""
