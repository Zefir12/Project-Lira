import socket
import pickle


class Client:
    def __init__(self, name, ip):
        self.server = ip
        self.port = 5000
        self.name = name
        self.addr = (self.server, self.port)
        self.client = socket.socket()
        self.id = None
        self.close_connection = False

    def connect(self):
        self.client.connect(self.addr)
        self.id = pickle.loads(self.client.recv(262144))
        self.client.send(pickle.dumps(self.name))

    def send(self, data, prinnt):
        self.client.send(data)
        dane = self.client.recv(262144)
        if prinnt:
            print(pickle.loads(dane))

        if self.close_connection:
            self.client.close()
        return pickle.loads(dane)