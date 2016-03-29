# -*- coding: utf-8 -*-
"""
:author: Pawel Kunat
:contact: pawel.kunat@nsn.com
"""


class OutOfScopeListener(object):

    def __init__(self, scope, callback):
        self._scope = scope
        self._callback = callback
        self._keyword_count = None
        self._keyword_arguments_fetched_count = 0
        self._keyword_documentation_fetched_count = 0

    def keyword_names_fetched(self, keyword_names):
        """Called when robot calls get_keyword_names() on the library"""
        self._keyword_count = len(keyword_names)

    def keyword_arguments_fetched(self, name):
        """Called when robot calls get_keyword_arguments(name) on the library"""
        self._keyword_arguments_fetched_count += 1
        self._check_if_metadata_instance_is_out_of_scope()

    def keyword_documentation_fetched(self, name):
        """Called when robot calls get_keyword_documentation(name) on the library"""
        self._keyword_documentation_fetched_count += 1
        self._check_if_metadata_instance_is_out_of_scope()

    def _check_if_metadata_instance_is_out_of_scope(self):
        if self._metadata_instance_is_out_of_scope():
            self._callback()

    def _metadata_instance_is_out_of_scope(self):
        return self._scope != 'GLOBAL' and \
            self._keyword_count == self._keyword_arguments_fetched_count and \
            self._keyword_count == self._keyword_documentation_fetched_count

    def close(self):
        """Called when a normal library instance (not the one used for getting kw metadata) goes out of scope."""
        self._callback()
