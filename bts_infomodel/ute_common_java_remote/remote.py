# -*- coding: utf-8 -*-
"""
:author: Pawel Kunat
:contact: pawel.kunat@nsn.com
"""
from ute_common_java_remote.listener import OutOfScopeListener
from ute_common_java_remote.server import JavaRemoteServer
from ute_common_java_remote.client import JavaRemoteClient, JavaRemoteAggregatingClient, DuplicateJavaKeywordException


class JavaRemote(object):

    ROBOT_LIBRARY_SCOPE = 'TEST SUITE'

    ROBOT_LISTENER_API_VERSION = 2

    def __init__(self, classpath, keyword_classes, **jvm_options):
        self.classpath = classpath
        self.keyword_classes = keyword_classes
        self.jvm_options = jvm_options
        self._server = None
        self._client = None
        self.ROBOT_LIBRARY_LISTENER = OutOfScopeListener(self.ROBOT_LIBRARY_SCOPE, self._tear_down_remote_if_necessary)

    def get_keyword_names(self):
        """Returns a list of available keywords."""
        self._set_up_remote_if_necessary()
        try:
            keyword_names = self._client.get_keyword_names()
        except DuplicateJavaKeywordException:
            self._tear_down_remote_if_necessary()
            raise
        self.ROBOT_LIBRARY_LISTENER.keyword_names_fetched(keyword_names)
        return keyword_names

    def run_keyword(self, name, args, kwargs):
        """Runs given keyword."""
        self._set_up_remote_if_necessary()
        return self._client.run_keyword(name, args, kwargs)

    def get_keyword_arguments(self, name):
        """Returns a list of argument names for given keyword."""
        self._set_up_remote_if_necessary()
        args = self._client.get_keyword_arguments(name)
        self.ROBOT_LIBRARY_LISTENER.keyword_arguments_fetched(name)
        return args

    def get_keyword_documentation(self, name):
        """Returns the documentation for given keyword."""
        self._set_up_remote_if_necessary()
        documentation = self._client.get_keyword_documentation(name)
        self.ROBOT_LIBRARY_LISTENER.keyword_documentation_fetched(name)
        return documentation

    def _set_up_remote_if_necessary(self):
        if not self._server:
            self._set_up_remote()

    def _set_up_remote(self):
        self._server = JavaRemoteServer(self.classpath, self.keyword_classes, **self.jvm_options)
        self._server.start()
        self._client = self._create_client(self._server.urls)

    def _create_client(self, classes_and_urls):
        clients = []
        for kw_class, url in classes_and_urls.items():
            clients.append(JavaRemoteClient(url, kw_class))
        if len(clients) == 1:
            return clients[0]
        else:
            return JavaRemoteAggregatingClient(clients)

    def _tear_down_remote_if_necessary(self):
        if self._server:
            self._server.stop()
