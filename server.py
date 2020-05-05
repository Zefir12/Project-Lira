import socket
import pickle
from _thread import *
from map import Map

map = Map('Land', 0)


class Server:
    def __init__(self):
        self.host = "192.168.0.7"
        self.port = 5000
        self.server = socket.socket()
        self.players = {}

    def bind(self, players):
        self.server.bind((self.host, self.port))
        self.server.listen(players)

    def threaded_client(self, conn, p):
        while True:
            try:
                data = conn.recv(1024)
                executable = pickle.loads(data)
                print(executable)
                self.players[executable['id']] = executable
            except:
                a = self.players[p]['name']
                print(f'Gracz {a} rozłączył sie')
                self.players.pop(p)
                break

            instructions = self.players
            dane = pickle.dumps(instructions)
            conn.send(dane)

    def responding_to_connection(self):
        p = 1
        while True:
            id = [p]
            conn, addr = self.server.accept()
            print("Connected to:", addr)
            conn.send(pickle.dumps(id))
            self.players[p] = {}
            self.players[p]['name'] = pickle.loads(conn.recv(1024))
            start_new_thread(self.threaded_client, (conn, p))
            p += 1


server = Server()
server.bind(5)
server.responding_to_connection()