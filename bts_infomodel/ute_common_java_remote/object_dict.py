# -*- coding: utf-8 -*-
"""
:author: Pawel Kunat
:contact: pawel.kunat@nsn.com
"""


class object_dict(dict):
    """A dictionary that allows attribute-based access (dictionary.key instead of dictionary['key'])."""

    def __getattr__(self, attr):
        attr = self[attr]
        return object_dict(attr) if isinstance(attr, dict) else attr

    def __setattr__(self, name, value):
        self[name] = value

    def __delattr__(self, name):
        del self[name]
