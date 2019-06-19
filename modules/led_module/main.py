from time import sleep

from common.signals import register_signal_callback
from client.comm import Comm
from modules.led_module.module.mod import Module


def main():
    print("Starting application...\n")
    module = Module(Comm())
    print("Module created...")

    with module:
        register_signal_callback(module.stop)
        while not module.stopped:
            module.process()
            sleep(0.05)



if __name__ == "__main__":
    main()
