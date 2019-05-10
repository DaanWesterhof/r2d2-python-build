from common.common import BusConfig
from time import sleep
from multiprocessing.managers import BaseManager
from multiprocessing import Lock
import os
import threading
import copy
import signal
from sys import platform


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

        print("Starting queue manager...")
        # Register the queue for receiving frames from modules
        QueueManager.register('rx_queue', callable=lambda: self.rx_queue)
        # Register the queue for sending frames to modules
        QueueManager.register('tx_queue', callable=lambda: self.tx_queue)
        self.manager = QueueManager(address=('', BusConfig.PORT), authkey=BusConfig.AUTH_KEY)
        self.server = self.manager.get_server()

        print("Start serving!")
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

            #print(frame)  # 'send'
            print()

    def _process_rx(self):
        """
        Function processes an incomming frame.
        The function locks the queue and copies the frame to an internal queue and after it releases the queue.
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
        print("Starting...")

        self.manager_thread.start()

        # Wait for the manager to start up...
        sleep(0.5)

        print("Starting consumer...")

        pusher = QueueManager(address=BusConfig.ADDRESS, authkey=BusConfig.AUTH_KEY)
        pusher.connect()

        print("Init done, working...")

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
