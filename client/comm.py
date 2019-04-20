from common.common import Frame, Priority, BusConfig, FrameWrapper
from common.frame_enum import FrameType
from queue import Queue
from time import time
import threading
import os

from multiprocessing.managers import BaseManager


class QueueManager(BaseManager):
    pass


QueueManager.register('rx_queue')
QueueManager.register('tx_queue')


class Comm:
    def __init__(self):
        self.manager = QueueManager(address=BusConfig.ADDRESS, authkey=BusConfig.AUTH_KEY)
        self.manager.connect()

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
                pid, timestamp = frame[0]

                print(self.pid, self.last_timestamp, frame)

                # If the PID equals this pid, we have sent this message
                # If the timestamp is older than our last timestamp, we have already
                # processed this message
                if self.pid == pid or timestamp <= self.last_timestamp:
                    continue

                self.last_timestamp = timestamp

                # TODO: check if we actually accepts this packet type
                if self.accepts_frame(frame[1].type):
                    self.received.put(frame[1])

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

    def listen_for(self, comm_listen_for: list):
        """
        Specify what frame types this modules
        should receive from the bus.

        :param listen_for:
        :return:
        """
        self.comm_listen_for = comm_listen_for

        if FrameType.ALL in comm_listen_for:
            self.accepts_all = True

    def accepts_frame(self, type: FrameType):
        """
        Does this modules accept the given
        frame type?

        :param type:
        :return:
        """
        if self.accepts_all:
            return True
        return type in self.comm_listen_for

    def request(self, type, prio: Priority = Priority.NORMAL):
        """
        Request data from the bus

        :param type:
        :param prio:
        :return:
        """
        frame = Frame()
        frame.type = type
        frame.request = True
        frame.priority = prio

        self._push_frame(frame)

    def send(self, frame, prio: Priority = Priority.NORMAL):
        """
        Put a frame on the bus.

        :param type:
        :param data:
        :param prio:
        """
        frame.request = False
        frame.priority = prio

        self._push_frame(frame)

    def has_data(self):
        """
        Whether there is data available for
        processing for this instance.

        :return:
        """

        return not self.received.empty()

    def get_data(self):
        """
        Non-blocking, will throw the Empty
        exception if no data is available.

        Check if there is data available for processing
        first with has_data.
        :return: common.Frame
        """

        item = self.received.get()
        self.received.task_done()
        return item

    def stop(self):
        self.should_stop = True
        self.channel_worker.join()
