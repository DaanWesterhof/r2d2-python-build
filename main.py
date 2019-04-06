# from module.led import Module
# from time import sleep
#
#
# def main():
#     print("Starting application...")
#     module = Module()
#     print("Module created...")
#
#     while True:
#         module.process()
#         sleep(1)
#

from multiprocessing.managers import BaseManager
from queue import Queue


class QueueManager(BaseManager):
    pass


QueueManager.register('get_queue')

if __name__ == "__main__":
    manager = QueueManager(address=('127.0.0.1', 5000), authkey=b'r2d2')
    manager.connect()

    queue = manager.get_queue()
    queue.put('hello')
    print(queue.get())
    queue.task_done()
    # main()
