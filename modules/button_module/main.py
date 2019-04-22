import signal
from random import randint
from time import sleep
from sys import platform
from modules.button_module.module.mod import Module

should_stop = False


class TestButton:
    def read(self):
        return randint(0, 1) == 1


def main():
    print("Starting application...")
    module = Module(TestButton())
    print("Module created...")

    while not should_stop:
        module.process()
        sleep(0.05)

    module.stop()


def stop(signal, frame):
    global should_stop
    should_stop = True


signal.signal(signal.SIGINT, stop)
signal.signal(signal.SIGTERM, stop)

if platform != "win32":
    signal.signal(signal.SIGQUIT, stop)

if __name__ == "__main__":
    main()
