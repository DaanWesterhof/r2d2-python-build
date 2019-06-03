"""this file executes the button_module program"""

from time import sleep
from sys import platform
from random import randint

from common.signals import register_signal_callback
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

    register_signal_callback(module.stop)

    with module:
        while not module.stopped:
            module.process()
            sleep(0.05)


if __name__ == "__main__":
    main()
