from module.led import Module
from time import sleep


def main():
    print("Starting application...")
    module = Module()
    print("Module created...")

    while True:
        module.process()
        sleep(1)


if __name__ == "__main__":
    main()
