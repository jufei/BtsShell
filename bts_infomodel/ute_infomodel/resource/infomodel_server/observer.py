# -*- coding: utf-8 -*-
"""
:created on: 28.02.14

:copyright: NSN
:author: Bartłomiej Idzikowski
:contact: bartlomiej.idzikowski@nsn.com
"""


class Observable(object):
    def __init__(self):
        self.observers = []

    def register(self, observer):
        """Register observer"""
        self.observers.append(observer)

    def unregister(self, observer):
        """Unregister observer"""
        self.observers.remove(observer)

    def notify_all(self, event):
        """Notify all observers about an event."""
        for observer in self.observers:
            observer.notify(event)
