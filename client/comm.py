from common.common import Frame, FrameType, Priority
from common.channel import Channel
from queue import Queue
import threading


class Comm:
    def __init__(self):
        self.channel = Channel()

        self.listen_for = []
        self.accepts_all = False
        self.rx_queue = Queue()

        # Start the worker thread for the
        # connection.
        self.channel_worker = threading.Thread(target=self._work_channel)
        self.channel_worker.start()

    def _work_channel(self):
        """
        This method is called as a worker thread.
        Create and work the communication channel to
        the bus.

        :return:
        """

        print("Starting connection worker...")

        self.channel = Channel()
        self.channel.connect()

        print("Tx channel connected. Waiting for data...")

        while True:
            self.channel.work()

            for frame in self.channel.get_received():
                self.rx_queue.put(frame)

    def _safely_push_frame(self, frame: Frame):
        """
        Push the frame on to the queue, if there is
        no space available on the queue this call will
        block until space is available again.

        :param frame:
        :return:
        """

        self.channel.queue_for_sending(frame)

    def listen_for(self, listen_for: list):
        """
        Specify what frame types this module
        should receive from the bus.

        :param listen_for:
        :return:
        """
        self.listen_for = listen_for

        if FrameType.ALL in listen_for:
            self.accepts_all = True

    def accepts_frame(self, type: FrameType):
        """
        Does this module accept the given
        frame type?

        :param type:
        :return:
        """
        if self.accepts_all:
            return True
        return type in self.listen_for

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

        self._safely_push_frame(frame)

    def send(self, type, data, prio: Priority = Priority.NORMAL):
        """
        Put a frame on the bus.

        :param type:
        :param data:
        :param prio:
        :return:
        """
        frame = Frame()
        frame.type = type

        # TODO: this is a temporary implementation
        #frame.set_data(data)
        frame.request = False
        frame.priority = prio

        self._safely_push_frame(frame)

    def has_data(self):
        """
        Whether there is data available for
        processing for this instance.

        :return:
        """

        return not self.rx_queue.empty()

    def get_data(self):
        """
        Non-blocking, will throw the Empty
        exception if no data is available.

        Check if there is data available for processing
        first with has_data.
        :return:
        """

        item = self.rx_queue.get(block=True, timeout=None)
        self.rx_queue.task_done()
        return item
