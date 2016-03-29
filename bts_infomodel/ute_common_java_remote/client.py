# -*- coding: utf-8 -*-
"""
:author: Pawel Kunat
:contact: pawel.kunat@nsn.com
"""
from robot.libraries.Remote import Remote
from ute_common_java_remote.object_dict import object_dict
from ute_common_java_remote.exception import DuplicateJavaKeywordException, JavaKeywordDoesNotExistException


class JavaRemoteClient(object):

    def __init__(self, url, keyword_class):
        self.keyword_class = keyword_class
        self._robot_remote = Remote(url)
        self._keyword_names = None
        self._keyword_arguments = {}
        self._keyword_documentation = {}

    def get_keyword_names(self):
        """Returns a list of available keywords."""
        if self._keyword_names is None:
            self._keyword_names = self._robot_remote.get_keyword_names()
            if 'stop_remote_server' in self._keyword_names:
                self._keyword_names.remove('stop_remote_server')
        return self._keyword_names

    def run_keyword(self, name, args, kwargs):
        """Runs given keyword."""
        result = self._robot_remote.run_keyword(name, args, kwargs)
        return self._wrap_if_dict(result)

    def _wrap_if_dict(self, value):
        return object_dict(value) if isinstance(value, dict) else value

    def get_keyword_arguments(self, name):
        """Returns a list of argument names for given keyword."""
        if name not in self._keyword_arguments:
            self._keyword_arguments[name] = self._robot_remote.get_keyword_arguments(name)
        return self._keyword_arguments[name]

    def get_keyword_documentation(self, name):
        """Returns the documentation for given keyword."""
        if name not in self._keyword_documentation:
            self._keyword_documentation[name] = self._robot_remote.get_keyword_documentation(name)
        return self._keyword_documentation[name]


class JavaRemoteAggregatingClient(object):
    """Dispatches get_keyword_names, get_keyword_arguments, get_keyword_documentation and run_keyword
       calls to actual clients
    """

    def __init__(self, clients):
        self._clients = clients
        self._keyword_names = None
        self._keywords_to_clients = None

    def _map_keywords_to_clients_if_necessary(self):
        if self._keyword_names is None:
            self._map_keywords_to_clients()

    def _map_keywords_to_clients(self):
        self._keyword_names = []
        self._keywords_to_clients = {}
        for client in self._clients:
            for keyword in self._get_normalized_keywords(client):
                self._map_keyword_to_client(keyword, client)

    def _map_keyword_to_client(self, keyword, client):
        if keyword in self._keywords_to_clients:
            raise DuplicateJavaKeywordException(keyword, client, self._keywords_to_clients[keyword])
        self._keyword_names.append(keyword)
        self._keywords_to_clients[keyword] = client

    def _get_normalized_keywords(self, client):
        keywords = client.get_keyword_names()
        normalized_keywords = [self._normalize(kw) for kw in keywords]
        return normalized_keywords

    def _normalize(self, name):
        return name.replace(' ', '').replace('_', '').lower()

    def get_keyword_names(self):
        """Returns a list of available keywords."""
        self._map_keywords_to_clients_if_necessary()
        return self._keyword_names

    def run_keyword(self, name, args, kwargs):
        """Runs given keyword."""
        self._map_keywords_to_clients_if_necessary()
        return self._get_client(name).run_keyword(name, args, kwargs)

    def get_keyword_arguments(self, name):
        """Returns a list of argument names for given keyword."""
        self._map_keywords_to_clients_if_necessary()
        return self._get_client(name).get_keyword_arguments(name)

    def get_keyword_documentation(self, name):
        """Returns the documentation for given keyword."""
        self._map_keywords_to_clients_if_necessary()
        return self._get_client(name).get_keyword_documentation(name)

    def _get_client(self, keyword):
        normalized_keyword = self._normalize(keyword)
        if normalized_keyword in self._keywords_to_clients:
            return self._keywords_to_clients[normalized_keyword]
        else:
            raise JavaKeywordDoesNotExistException(keyword)
