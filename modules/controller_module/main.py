"""this file executes the controller_module"""
from time import sleep
from sys import platform
import signal

from client.comm import Comm
from modules.controller_module.module.mod import Module

SHOULD_STOP = False


def main():
    """symbolic main"""
    print("Starting application...\n")
    module = Module(Comm())
    print("Module created...")

    while not SHOULD_STOP:
        module.process()
        sleep(0.05)

    module.stop()


def stop(signal, frame):
    """
    Stops the process and  stops the listening to incoming frames
    :return:
    """
    global SHOULD_STOP
    SHOULD_STOP = True


signal.signal(signal.SIGINT, stop)
signal.signal(signal.SIGTERM, stop)

if platform != "win32":
    signal.signal(signal.SIGQUIT, stop)

if __name__ == "__main__":
    main()
