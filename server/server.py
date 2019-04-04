import zmq
from common.common import Frame


context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind('tcp://127.0.0.1:5555')

while True:
    msg = socket.recv()
    print(msg)
    frame = Frame()
    frame.length = 2
    socket.send_pyobj(frame)