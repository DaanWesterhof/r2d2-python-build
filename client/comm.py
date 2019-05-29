"""
this module provides the API to the python bus
"""

from queue import Queue
from time import time
import threading
import os
from multiprocessing.managers import BaseManager
from abc import abstractclassmethod, ABC
import logging

from common.common import Frame, Priority, BusConfig, FrameWrapper
from common.frame_enum import FrameType


FORMAT = '%(asctime)s %(levelname)s: %(message)s'
logging.basicConfig(format=FORMAT)
COMM_LOGGER = logging.getLogger("python_build.comm")

class BaseComm(ABC):
    """
    Interface for communication classes.
    """
    @abstractclassmethod
    def listen_for(self, comm_listen_for: list) -> None:
        """
        Specify what frame types this modules
        should receive from the bus.

        :param comm_listen_for:
        :return:
        """

    @abstractclassmethod
    def accepts_frame(self, frame_type: FrameType) -> bool:
        """
        Does this modules accept the given
        frame type?

        :param type:
        :return:
        """

    @abstractclassmethod
    def request(self, frame_type: FrameType, prio: Priority = Priority.NORMAL) -> None:
        """
        Request data from the bus

        :param type:
        :param prio:
        :return:
        """

    @abstractclassmethod
    def send(self, frame, prio: Priority = Priority.NORMAL) -> None:
        """
        Put a frame on the bus.

        :param type:
        :param data:
        :param prio:
        """

    @abstractclassmethod
    def has_data(self) -> bool:
        """
        Whether there is data available for
        processing for this instance.

        :return:
        """

    @abstractclassmethod
    def get_data(self) -> Frame:
        """
        Non-blocking, will throw the Empty
        exception if no data is available.

        Check if there is data available for processing
        first with has_data.
        :return: common.Frame
        """

    @abstractclassmethod
    def stop(self) -> None:
        pass


class QueueManager(BaseManager):
    pass


QueueManager.register('rx_queue')
QueueManager.register('tx_queue')


class Comm(BaseComm):
    def __init__(self):
        self.manager = QueueManager(address=BusConfig.ADDRESS, authkey=BusConfig.AUTH_KEY)
        try:
            self.manager.connect()
        except ConnectionRefusedError:
            COMM_LOGGER.fatal("could not connect to python bus, did you start manager/manager.py?", exc_info=True)
            COMM_LOGGER.fatal("gracefull shutdown because of https://github.com/R2D2-2019/r2d2-python-build/issues/56")
            exit()

        # Queues that refer to the bus process
        self.rx_queue = self.manager.rx_queue()
        self.tx_queue = self.manager.tx_queue()
        self.last_timestamp = 0

        self.comm_listen_for = []
        self.accepts_all = False
        self.received = Queue()

        # Start the worker thread for the
        # connection.
        self.should_stop = False
        self.channel_worker = threading.Thread(target=self._work_channel)
        self.channel_worker.start()

        self.pid = os.getpid()

    def _work_channel(self):
        """
        This method is called as a worker thread.
        Create and work the communication channel to
        the bus.

        :return:
        """

        print("Starting connection worker...")

        while not self.should_stop:
            for frame in self.rx_queue._getvalue():
                # If the PID equals this pid, we have sent this message
                # If the timestamp is older than our last timestamp, we have already
                # processed this message
                if self.pid == frame.pid or frame.timestamp <= self.last_timestamp:
                    continue

                self.last_timestamp = frame.timestamp

                # Frame is of the type "FrameWrapper" which has the
                # actual "Frame" instance in the member frame.
                frame = frame.frame

                if self.accepts_frame(frame.type):
                    self.received.put(frame)

    def _push_frame(self, frame: Frame):
        """
        Push the frame on to the queue, if there is
        no space available on the queue this call will
        block until space is available again.

        :param frame:
        :return:
        """

        self.tx_queue.append(
            FrameWrapper(frame, self.pid, time())
        )

    def listen_for(self, comm_listen_for: list) -> None:
        self.comm_listen_for = comm_listen_for

        if FrameType.ALL in comm_listen_for:
            self.accepts_all = True

    def accepts_frame(self, type: FrameType) -> bool:
        if self.accepts_all:
            return True
        return type in self.comm_listen_for

    def request(self, type, prio: Priority = Priority.NORMAL) -> None:
        frame = Frame()
        frame.type = type
        frame.request = True
        frame.priority = prio

        self._push_frame(frame)

    def send(self, frame, prio: Priority = Priority.NORMAL) -> None:
        frame.request = False
        frame.priority = prio

        self._push_frame(frame)

    def has_data(self) -> bool:
        return not self.received.empty()

    def get_data(self) -> Frame:
        item = self.received.get()
        self.received.task_done()
        return item

    def stop(self) -> None:
        """
        Stop the worker thread.
        :return:

        """
        self.should_stop = True
        self.channel_worker.join()
