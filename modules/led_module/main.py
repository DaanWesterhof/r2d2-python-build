from modules.led_module.module.led import Module
from time import sleep
import signal

should_stop = False


def main():
    print("Starting application...")
    module = Module()
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
signal.signal(signal.SIGQUIT, stop)

if __name__ == "__main__":
    main()
