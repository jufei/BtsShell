# -*- coding: utf-8 -*-
"""
:author: Pawel Chomicki
:contact: pawel.chomicki@nsn.com
"""
class StoreException(Exception):
    """Store base exception"""


class NameIsProtected(Exception):
    """Exception raised when key is tried to be overridden."""


class AliasError(Exception):
    """Exception raised if alias doesn't exist."""


class Store(object):
    """Class to build object needed to add/remove/show/protect objects.

    .. code-block:: python

        store = Store()                          # Create new store

        store.add("Some object")                 # Adds object under "default" alias
        store.add("Some object", alias='test')   # Adds object under "test" alias

        store.get()                              # Returns object represented by "default" alias
        store.get(alias='test')                  # Returns object represented by "test" alias

        store.remove()                           # Removes object represented by "default" alias
        store.remove(alias='test')               # Removes object represented by "test" alias

        aliases = store.aliases                  # Returns list of available aliases
    """

    def __init__(self):
        self._objects = {}

    @property
    def aliases(self):
        """Property to get all available aliases.

        :return: List of available aliases.
        :rtype: list
        """
        return self._objects.keys()

    def add(self, value, alias=None):
        """Add new object to store and protect it to be not overridden.

        :param value:         Some object to store.
        :param string alias:  Alias (reference) for stored object.
                              Alias "default" is reserved and is used when alias is not specified.
        """
        alias = self._get_alias(alias)
        if alias in self._objects:
            raise NameIsProtected("Alias ({}) exists. Please remove it to reuse.".format(alias))
        self._objects[alias] = value
        self.show_alias()


    def remove(self, alias=None):
        """Remove object stored under specified name.

        :param string alias: Alias (reference) for stored object.
                             Alias "default" is reserved and is used when alias is not specified.
        """
        alias = self._get_alias(alias)
        if alias not in self._objects:
            raise AliasError("Provided alias ({}) doesn't exist. "
                             "Please setup library before any other operation.".format(alias))
        del self._objects[alias]
        self.show_alias()

    def get(self, alias=None):
        """Returns object specified by the name.

        :param string alias: Alias (reference) for stored object.
                             Alias "default" is reserved and is used when alias is not specified.

        :return: Object represented by specified alias or represented by "default" alias
        """
        alias = self._get_alias(alias)
        if alias not in self._objects:
            raise AliasError("Provided alias ({}) doesn't exist. "
                             "Please setup library before any other operation.".format(alias))
        return self._objects[alias]

    def _get_alias(self, alias):
        return "default" if alias is None else alias

    def show_alias(self):
        try:
            import time
            with open('/tmp/info.log', 'a') as f:
                aliaslist = self._objects.keys()
                aliaslist.sort()
                f.write('\n' + time.strftime("%Y_%m_%d__%H_%M_%S")+'\n')
                if aliaslist:
                    for alias in aliaslist:
                        f.write('       '+ alias + '\n')
                else:
                    f.write('   No any alias\n')
        except:
            pass

