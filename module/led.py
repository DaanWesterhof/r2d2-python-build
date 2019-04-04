from client.comm import Comm


class Module:
    def __init__(self):
        self.comm = Comm()

    def process(self):
        while self.comm.has_data():
            frame = self.comm.get_data()

            print(frame)
