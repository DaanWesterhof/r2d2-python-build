#! python
"""
this program hosts the python internal bus.

see client/comm.py for the interface
"""

from sys import platform
import os
import copy
import threading
import signal
import logging
from time import sleep
from multiprocessing.managers import BaseManager
from multiprocessing import Lock
from common.common import BUSCONFIG
import common.config

class QueueManager(BaseManager):
    """
    Alias for the object pool for sharing the inter process
    objects
    """
    pass


PACKET_QUEUE_LENGTH = 64


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

        self.tx_queue = []
        """Transmitting queue"""

        self.manager = None
        """Contains the object pool/manager"""

        self.manager_thread = threading.Thread(target=self._manager)
        """The thread where the manager runs in."""

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
        self.manager = QueueManager(address=('', BUSCONFIG.ADDRESS.port), authkey=BUSCONFIG.AUTH_KEY)
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
            #self.rx_queue.append(frame)
        else:
            self.rx_queue.pop(0)

        self.processing_lock.release()

    def start(self):
        """
        Starts the manager and exposes a central bus.

        :return:
        """
        _LOGGER.info("Starting...")

        self.manager_thread.start()

        # Wait for the manager to start up...
        sleep(0.5)

        _LOGGER.info("Starting consumer...")

        pusher = QueueManager(address=BUSCONFIG.ADDRESS.tuple(), authkey=BUSCONFIG.AUTH_KEY)
        pusher.connect()

        _LOGGER.info("Init done, working...")

        while not self.should_stop:
            self._process_tx()
            self._process_rx()
            sleep(0.01)

    def stop(self):
        """
        Stops the manager thread

        :return:
        """
        self.should_stop = True
        self.server.stop_event.set()
        self.manager_thread.join()

bus_manager = BusManager()

_LOGGER = logging.getLogger("manager.manager")

def stop(signal, frame):
    """
    Stops the bus manager.

    :return:
    """
    bus_manager.stop()


signal.signal(signal.SIGINT, stop)
signal.signal(signal.SIGTERM, stop)

if platform != "win32":
    signal.signal(signal.SIGQUIT, stop)

bus_manager.start()
