#! python

"""this file demonstrates socket communication over the python bus
the tests in this file assumes that manager/manager.py is running in the background.
"""

import socket
import logging
import random
import struct
import threading
import time
from datetime import date
from dataclasses import dataclass

import pytest

from manager.manager import BusManager
from client.comm import Comm
from common.frame_enum import FrameType
from common.frames import FrameButtonState
from common.frame_enum_mapping import MAPPING


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


@pytest.mark.order1
def test_socket():
    """tests the socket"""
    adress = Adress("localhost", 4999)
    seed = random.randint(0, 100)
    logging.basicConfig(level=logging.DEBUG)
    server_thread = threading.Thread(target=server, args=(adress, seed))
    server_thread.start()
    assert client(adress) == seed
    server_thread.join()

@pytest.mark.order2
def test_python_bus():
    """verifies that the bus manager and comm object talk with each other"""
    with Comm(False) as rx_comm, Comm() as tx_comm:
        rx_comm.listen_for([FrameType.ALL])
        frame = FrameButtonState()
        frame.set_data(True)
        tx_comm.send(frame)
        rframe = rx_comm.get_data()
        assert frame.get_data() == rframe.get_data()

@pytest.mark.order3
def test_incomming_socket():
    """verifies that the python bus can receive frames from external comunication"""
    with Comm(False) as rx_comm:
        rx_comm.listen_for([FrameType.ALL])
        
        sock = socket.socket()
        sock.connect(("localhost", 5010))
        sock.send(struct.pack("BBBI", 1, 0, 0, FrameType.BUTTON_STATE.value))
        sock.send(struct.pack("?", True))
        time.sleep(0)
        ack = sock.recv(1)
        assert ack
        sock.close()
        while not rx_comm.has_data():
            time.sleep(1)
        assert rx_comm.has_data()
        frame = rx_comm.get_data()
        assert frame.type == FrameType.BUTTON_STATE
        assert frame.get_data() == (True,)

@pytest.mark.order4
def test_outgoing_socket():
    with Comm() as tx_comm:
        frame = FrameButtonState()
        frame.set_data(True)
        tx_comm.send(frame)

        header_pattern = b"BBBI"

        sock = socket.socket()
        sock.connect(("localhost", 5020))
        header = sock.recv(8)

        length, octet_3, octet_4, frame_type = struct.unpack(header_pattern, header)
        frame_type = FrameType(value=frame_type)
        frame = MAPPING[frame_type]()
        
        frame.data = sock.recv(length)
        sock.send(b"1")
        sock.close()

        assert frame.get_data() == (True,)
