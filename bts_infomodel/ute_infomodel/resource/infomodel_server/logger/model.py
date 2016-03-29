# -*- coding: utf-8 -*-
"""
:created on: 27.02.14

:copyright: NSN
:author: Bartłomiej Idzikowski
:contact: bartlomiej.idzikowski@nsn.com
"""


from java.io import File, FileOutputStream
from com.nsn.oam.infomodel.communication.ims2 import IMS2DiscreteRecorder


class LoggerModel(object):
    LOG_FORMATS = ['ims2']

    def __init__(self, model):
        self.model = model
        self.recorder = IMS2DiscreteRecorder(self.model.provider)

    def start(self):
        """Start infomodel logger."""
        self.model.provider.registerListener(self.recorder)

    def stop(self):
        """Stop infomodel logger."""
        self.model.provider.unregisterListener(self.recorder)

    def save(self, filename, log_format):
        """Save infomodel log.

        :param string filename: Filename or path to the log file.
        :param string log_format: Log format. Currently only ims2 is available.
        """
        filename = filename if filename.endswith(".ims2") else "%s.ims2" % filename
        log_format = log_format if log_format in LoggerModel.LOG_FORMATS else 'ims2'
        self.recorder.save(FileOutputStream(File(filename)))

    def clean(self):
        """Clean infomodel log."""
        self.model.provider.unregisterListener(self.recorder)
        self.recorder = IMS2DiscreteRecorder(self.model.provider)
        self.model.provider.registerListener(self.recorder)
