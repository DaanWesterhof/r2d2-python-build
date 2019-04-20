from common.common import BusConfig
from time import time, sleep
from multiprocessing.managers import BaseManager
from multiprocessing import Lock
from common.frames import FrameButtonState
import os
import threading
import copy
import signal


class QueueManager(BaseManager):
    pass


class BusServer:
    def __init__(self):
        self.processing_lock = Lock()
        self.should_stop = False

        self.rx_queue = []
        self.tx_queue = []

        self.manager = None
        self.manager_thread = threading.Thread(target=self._manager)
        self.server = None
        self.pid = os.getpid()

    def _manager(self):
        """
        Called from a separate thread.

        :return:
        """

        print("Starting queue manager...")

        QueueManager.register('rx_queue', callable=lambda: self.rx_queue)
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

        self.processing_lock.acquire()

        to_send = copy.deepcopy(self.tx_queue)
        self.tx_queue.clear()

        self.processing_lock.release()

        for frame in to_send:
            # Distribute frame internally
            frame = ((self.pid, time()), frame)
            self.rx_queue.append(frame)

            print(frame)  # 'send'
            print()

    def _process_rx(self):
        self.processing_lock.acquire()

        if len(self.rx_queue) <= 32:
            pass
            # TODO: socket
            #frame = ((self.pid, time()), FrameButtonState())
            #self.rx_queue.append(frame)
        else:
            self.rx_queue.pop(0)

        self.processing_lock.release()

    def start(self):
        print("Starting...")

        # self._manager()
        self.manager_thread.start()

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
        self.should_stop = True
        self.server.stop_event.set()
        self.manager_thread.join()


server = BusServer()


def stop(signal, frame):
    server.stop()


signal.signal(signal.SIGINT, stop)
signal.signal(signal.SIGTERM, stop)
signal.signal(signal.SIGQUIT, stop)

server.start()
