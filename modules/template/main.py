"this module is a template"
import time

from common.signals import register_signal_callback
from client.comm import Comm
from modules.template.module.mod import Module

def main():
    "entry point of the application"

    print("Starting application...\n")
    module = Module(Comm())
    register_signal_callback(module.stop)
    print("Module created...")
    with module:
        while not module.stopped:
            module.process()
            time.sleep(0.05)

if __name__ == "__main__":
    main()
