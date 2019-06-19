"""this file executes the controller_module"""
from time import sleep
from sys import platform

from common.signals import register_signal_callback
from client.comm import Comm
from modules.controller_module.module.mod import Module

def main():
    """symbolic main"""
    print("Starting application...\n")
    module = Module(Comm())
    print("Module created...")
    register_signal_callback(module.stop)
    with module:
        while not module.stopped:
            module.process()
            sleep(0.05)



if __name__ == "__main__":
    main()
