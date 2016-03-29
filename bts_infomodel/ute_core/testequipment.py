# -*- coding: utf-8 -*-
"""
:author: Pawel Chomicki
:contact: pawel.chomicki@nsn.com
"""
from abc import ABCMeta, abstractmethod


class TestEquipment(object):
    """Class defines common interface where business logic should be placed."""
    __metaclass__ = ABCMeta

    @abstractmethod
    def setup(self, *args, **kwargs):
        """ Method defines logic to prepare environment to work with specific object."""

    @abstractmethod
    def teardown(self, *args, **kwargs):
        """ Method defines logic to cleanup environment after object work is done."""
