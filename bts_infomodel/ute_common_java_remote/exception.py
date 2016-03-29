# -*- coding: utf-8 -*-
"""
:author: Pawel Kunat
:contact: pawel.kunat@nsn.com
"""
from ute_core.exception import CoreException


class JavaRemoteException(CoreException):
    """Base exception for the ute_common_java_remote library."""


class RemoteJavaServerFailedToStartException(JavaRemoteException):
    """Raised when the remote Java server cannot start or cannot bind required port(s)."""


class DuplicateJavaKeywordException(JavaRemoteException):
    """Raised when there are two keyword classes with the same method, which creates an ambiguity that cannot be resolved."""

    def __init__(self, keyword_name, client1, client2):
        self.keyword_name = keyword_name
        self.client1 = client1
        self.client2 = client2

    def __str__(self):
        return 'Keyword "%s" is defined both in %s and %s' % (self.keyword_name, self.client1.keyword_class, self.client2.keyword_class)


class JavaKeywordDoesNotExistException(JavaRemoteException):
    """Raised when JavaRemoteClient is asked to perform an action on a keyword that is not defined in any of the keyword classes."""

    def __init__(self, keyword_name):
        self.keyword_name = keyword_name

    def __str__(self):
        return 'Keyword "%s" is not defined in any of the keyword classes' % self.keyword_name
