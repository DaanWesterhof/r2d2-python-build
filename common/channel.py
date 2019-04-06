from queue import Queue

from multiprocessing import Pipe

class Channel:
    """
    Bidirectional communication channel.
    This channel uses two REP/REQ ZeroMQ sockets with separate contexts.
    """

    def __init__(self):
        self.pipe = Pipe()
        self.tx = Pipe()
        self.rx = Pipe()

        self.tx_queue = Queue()
        self.rx_queue = Queue()

    def connect(self):
        """
        Connect the channel to the bus.
        :return:
        """

        self.tx_conn.connect()

    def work(self):
        """
        Work the channel until there is no more
        work to be done.

        :return:
        """

        # Check if there is any data to be
        # received
        while self.rx_conn.has_data():
            data = self.rx_conn.receive()

            # Can be None
            if data:
                self.rx_queue.put(data)
                self.rx_conn.send(DummyResponse)

        # Send any frames that are queued
        # to be send.
        while not self.tx_queue.empty():
            data = self.tx_queue.get()

            if data:
                self.tx_conn.send(data)

                # Due to the nature of ZMQ sockets,
                # a receive is required here. A dummy packet
                # will be send.
                self.tx_conn.receive()

            self.tx_queue.task_done()

    def get_received(self):
        """
        Thread safe. Produce a list of
        all received frames. If no frames were
        received, an empty list is returned.

        :return:
        """

        frames = []

        while not self.rx_queue.empty():
            frames.append(self.rx_queue.get())
            self.rx_queue.task_done()

        return frames

    def queue_for_sending(self, frame):
        """
        Thread safe. Place the given frame on
        the tx queue.

        :param frame:
        :return:
        """

        self.tx_queue.put(frame)
