#! python
"""
this program hosts the python internal bus.

see client/comm.py for the interface
"""

import os
import copy
import threading
import time
import logging
from multiprocessing.managers import BaseManager
from multiprocessing import Lock
import socket
import struct
from common.frame_enum import FrameType
from common.frame_enum_mapping import MAPPING
from common.signals import register_signal_callback
from common.common import BUSCONFIG, FrameWrapper
import common.config # pylint: disable=unused-import


class QueueManager(BaseManager):
    """
    Alias for the object pool for sharing the inter process
    objects
    """



PACKET_QUEUE_LENGTH = 64
_LOGGER = logging.getLogger("manager.manager")


class BusManager:
    """
    The manager of the bus.
    Puts data on the bus and returns it from the bus.
    """

    def __init__(self):
        """
        Setup the manager
        Initializes the RX and TX queue
        Creates a place for the manager
        Creates a manager thread
        :return:
        """

        self.processing_lock = Lock()
        """ The lock on the queue, if locked no one can use the queue """

        self.should_stop = False
        """Contains if the bus must be ended."""

        self.rx_queue = []
        """Receiving queue"""

        self.rx_sock = socket.socket()

        self.tx_queue = []
        """Transmitting queue"""

        self.tx_sock = socket.socket()
        self.tx_sock_queue = []

        self.manager = None
        """Contains the object pool/manager"""

        self.manager_thread = threading.Thread(target=self._manager)
        """The thread where the manager runs in."""

        self.rx_sock_thread = threading.Thread(target=self._socket_rx)
        self.tx_sock_thread = threading.Thread(target=self._socket_tx)

        self.server = None
        self.pid = os.getpid()

    def _manager(self):
        """
        Bootstrap code for the manager.
        Called from a separate thread.

        :return:
        """
        _LOGGER.info("Starting queue manager...")
        # Register the queue for receiving frames from modules
        QueueManager.register('rx_queue', callable=lambda: self.rx_queue)
        # Register the queue for sending frames to modules
        QueueManager.register('tx_queue', callable=lambda: self.tx_queue)
        self.manager = QueueManager(
            address=('', BUSCONFIG.ADDRESS.port), authkey=BUSCONFIG.AUTH_KEY)
        self.server = self.manager.get_server()

        _LOGGER.info("Start serving!")
        self.server.serve_forever()

    def _process_tx(self):
        """
        Processing tx for the manager thread.
        Will deep copy all frames and release the lock.
        This prevents problems where the network socket is blocking
        modules needlessly.

        :return:
        """
        # Get a lock (mutex) on the transmitting queue
        self.processing_lock.acquire()

        to_send = copy.deepcopy(self.tx_queue)
        self.tx_queue.clear()

        self.processing_lock.release()

        for frame in to_send:
            # Distribute frame internally
            self.rx_queue.append(frame)
            self.tx_sock_queue.append(frame)

            _LOGGER.debug(frame)  # 'send'

    def _process_rx(self):
        """
        Function processes an incomming frame.
        The function locks the queue,
        then it copies the frame to an internal queue.
        after that it releases the queue.

        :return:
        """
        self.processing_lock.acquire()

        if len(self.rx_queue) <= PACKET_QUEUE_LENGTH:
            pass
            # TODO: socket
            #frame = ((self.pid, time()), FrameButtonState())
            # self.rx_queue.append(frame)
        else:
            self.rx_queue.pop(0)

        self.processing_lock.release()

    def _socket_rx(self):
        """
        receives frames over socket and puts them on the python bus


        current socket header format is (length: byte, unused: byte, unused: byte, frame type: int)

        the body is frame type dependant, but the length in bytes is equal to the header length

        acknowledgement is either a zero caracter '0' or a one caracter '1'


        on a socket the protocol for the remote is.
        1. connect to the python bus at port 5010
        2. send header
        3. send body
        4. recieve acknowledgement
        5. close connection (it will also be closed on the python bus)
        """
        header_pattern = b"BBBI"
        while not self.should_stop:
            time.sleep(0)
            connection, adress = self.rx_sock.accept()

            #! assumes connection responds
            header = connection.recv(struct.calcsize(header_pattern))
            self.processing_lock.acquire()

            try:
                length, octet_3, octet_4, frame_type = struct.unpack(header_pattern, header)
                frame_type = FrameType(value=frame_type)
            except struct.error:
                # ignore ill formed headers
                continue
            except ValueError:
                # ignore unknown frame type
                continue
            else:
                frame = MAPPING[frame_type]()
            #! assumes connection responds
            self.processing_lock.release()
            body = connection.recv(8*length)
            self.processing_lock.acquire()
            frame.data = body
            frame_wrapper = FrameWrapper(frame, os.getpid(), time.time())

            self.rx_queue.append(frame_wrapper)
            self.processing_lock.release()
            connection.send(b"1")

    def _socket_tx(self):
        """
        receives frames over socket and puts them on the python bus


        current socket header format is (length: byte, unused: byte, unused: byte, frame type: int)

        the body is frame type dependant, but the length in bytes is equal to the header length

        acknowledgement is either a zero caracter '0' or a one caracter '1'


        on a socket the protocol for the remote is.
        1. connect to the python bus at port 5020
        2. receive header
        3. receive body
        4. send acknowledgement
        5. close connection (it will also be closed on the python bus)

        the manager keeps breaking connections after each send frame.
        the manager also sends each frame only once to one connection.
        """
        while not self.should_stop:
            while self.tx_sock_queue:
                frame_wrapper = self.tx_sock_queue.pop()
                frame = frame_wrapper.frame
                header = struct.pack("BBBI", struct.calcsize(frame.format), 0, 0, frame.type.value)
                body = frame.data
                time.sleep(0)
                connection, address = self.tx_sock.accept()
                connection.send(header)
                connection.send(body)
                ack = connection.recv(1)
                assert ack
                connection.close()

    def __enter__(self):
        """
        Starts the manager and exposes a central bus.

        :return:
        """
        _LOGGER.info("Starting...")

        self.manager_thread.start()

        # Wait for the manager to start up...
        time.sleep(0.5)

        _LOGGER.info("Starting consumer...")

        pusher = QueueManager(
            address=BUSCONFIG.ADDRESS.tuple(), authkey=BUSCONFIG.AUTH_KEY)
        pusher.connect()

        _LOGGER.info("Starting sockets")

        self.rx_sock.bind((BUSCONFIG.ADDRESS.ip, 5010))
        self.rx_sock.listen(10)

        self.rx_sock_thread.start()

        self.tx_sock.bind((BUSCONFIG.ADDRESS.ip, 5020))
        self.tx_sock.listen(10)
        self.tx_sock_thread.start()


        _LOGGER.info("Init done, working...")
        return self

    def process(self):
        """processes both the receive and the send queue until stop is called"""
        while not self.should_stop:
            self._process_tx()
            self._process_rx()
            time.sleep(0.01)

    def __exit__(self, *args):
        self.should_stop = True
        self.server.stop_event.set()
        self.manager_thread.join()
        self.rx_sock_thread.join()
        self.tx_sock_thread.join()

    def stop(self):
        """
        Stops the manager thread

        :return:
        """
        self.should_stop = True


if __name__ == "__main__":
    with BusManager() as bus_manager:
        register_signal_callback(bus_manager.stop)
        bus_manager.process()
