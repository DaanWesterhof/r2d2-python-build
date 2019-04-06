from multiprocessing.managers import BaseManager
from queue import Queue


class QueueManager(BaseManager):
    pass


queue = Queue()

QueueManager.register('get_queue', callable=lambda: queue)

manager = QueueManager(address=('', 5000), authkey=b'r2d2')
server = manager.get_server()
server.serve_forever()
