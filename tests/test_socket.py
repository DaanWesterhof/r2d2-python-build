#! python

"""this file try's to demonstrate socket module"""

import socket
import logging
import random
import struct
import threading
from datetime import date
from dataclasses import dataclass


__author__ = "Isha Geurtsen"
__date__ = date(2019, 6, 20)
__status__ = "Prototyping"

@dataclass
class Adress:
    """ip4 address"""
    ip: str
    port: int

    def tuple(self)->tuple:
        "return address as a tuple, used for socket"
        return (self.ip, self.port)


def server(adress, seed):
    """binds a socket to address. sends seed to first connection, then shuts down"""
    logger = logging.getLogger("socket.server")
    logger.info("seed = %s", str(seed))
    with socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM) as sock:
        sock.bind(adress.tuple())
        sock.listen(5)
        logger.warning("bound %s to server, accepting connections", adress)
        connection, address_info = sock.accept()
        del address_info
        connection.send(struct.pack("B", seed))
    logger.warning("shutting down server")

def client(adress):
    """connect a socket to adress recieves one int and returns that int"""
    logger = logging.getLogger("socket.client")
    with socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM) as sock:
        sock.connect(adress.tuple(), )
        logger.info("connected to server")
        logger.info("awaiting seed")
        seed = struct.unpack("B", sock.recv(1))[0]
        logger.info("received seed %i", seed)
        return seed
    logger.warning("shutting down client")


def test_socket():
    """tests the socket"""
    adress = Adress("localhost", 5000)
    seed = random.randint(0, 100)
    logging.basicConfig(level=logging.DEBUG)
    server_thread = threading.Thread(target=server, args=(adress, seed))
    server_thread.start()
    assert client(adress) == seed
    server_thread.join()
