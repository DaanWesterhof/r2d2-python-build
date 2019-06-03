#! python

"""this file declares the base module"""

import datetime
from abc import ABC, abstractmethod
from client.comm import BaseComm
from common.signals import register_signal_callback

__author__ = "Isha Geurtsen"
__date__ = datetime.datetime(2019, 6, 3, 18, 47)
__status__ = "Development"

class BaseModule(ABC):
    """base application module"""
    def __init__(self, comm: BaseComm):
        self.comm = comm
        self.stopped = False
        register_signal_callback(self.stop)

    @abstractmethod
    def process(self):
        """the process function processes all outstanding work.
        Just like the C++ internal communication module,

        Please note: if you don't process data often enough, you might miss some frames.
        It is dependent on the module if this is a problem or not.
        """
        assert not self.stopped
        raise NotImplementedError

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.stopped = True
        self.comm.stop()

    def stop(self):
        """signals the application that it should shut down"""
        self.stopped = True
