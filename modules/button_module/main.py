"""this file executes the button_module program"""

from time import sleep
from sys import platform
from random import randint
import signal

from client.comm import Comm
from modules.button_module.module.mod import Module

SHOULD_STOP = False

class TestButton:
    """
    Button-dummy class that returns random True and False values on read.
    """
    def read(self):
        """
        Reads the button value. In this case the value is random.

        :return True: Button is pressed
        :return False: Button is unpressed
        """
        return randint(0, 1) == 1


def main():
    """
    Main function that starts the module

    :return:
    """
    print("Starting application...\n")
    module = Module(Comm(), TestButton())
    print("Module created...")

    while not SHOULD_STOP:
        module.process()
        sleep(0.05)

    module.stop()


def stop(signal, frame):
    """
    Stops the process and  stops the listening to incoming frames
    """
    global SHOULD_STOP
    SHOULD_STOP = True


signal.signal(signal.SIGINT, stop)
signal.signal(signal.SIGTERM, stop)

if platform != "win32":
    signal.signal(signal.SIGQUIT, stop)

if __name__ == "__main__":
    main()
