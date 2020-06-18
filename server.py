import socket
import pickle
from _thread import *
from map import *
import json
from os import path
import os

map = Map('Land', 0, 0)

"""if not path.exists(f"chunks/{position}.json"):
    with open(f"chunks/{position}.json", 'w') as f:
        json.dump(map.chunklist[position].save_chunk_into_json(), f)

if path.exists(f"chunks/{position}.json"):
    with open(f"chunks/{position}.json", 'w') as f:
        chunk = json.load(f)"""


class Server:
    def __init__(self):
        self.host = "192.168.0.5"
        self.port = 5000
        self.server = socket.socket()
        self.players = {}

    def bind(self, players):
        self.server.bind((self.host, self.port))
        self.server.listen(players)

    def threaded_client(self, conn, p):
        while True:
            try:
                data = conn.recv(262144)
                player_instructions = pickle.loads(data)
                if len(player_instructions['orders']['load_chunk']) > 0:
                    for position in player_instructions['orders']['load_chunk']:
                        if position not in map.chunklist:
                            map.chunklist[position] = map.create_chunk(position[0], position[1]).save_chunk_into_json()
                            map.generated_chunks.append(position)

                        player_instructions['send_chunks'].append(map.chunklist[position])

                self.players[player_instructions['id']] = player_instructions
                print(self.players)
            except:
                a = self.players[p]['name']
                print(f'Gracz {a} rozłączył sie')
                self.players.pop(p)
                if len(self.players) < 1:
                    start_new_thread(self.save_chunks_to_files, ())
                    self.save_map_file()
                break

            commands_to_all = self.players
            dane = pickle.dumps(commands_to_all)
            conn.send(dane)

    def save_chunks_to_files(self):
        for position in map.chunklist:
            if not path.exists(f"maps/{map.name}/chunks/{position}.json"):
                with open(f"maps/{map.name}/chunks/{position}.json", 'w') as f:
                    json.dump(map.chunklist[position], f)
                    map.chunks_saved_into_files.append(f'{position}.json')

    def clear_memory(self):
        for position in map.chunklist:
            map.chunklist.pop(position)

    def initialization(self):
        with os.scandir(f'maps/{map.name}/chunks') as entries:
            for entry in entries:
                print(entry.name)
                map.chunks_saved_into_files.append(entry.name)

    def save_map_file(self):
        map_file = {'name': map.name,  'seed': map.map_seed, 'identyfikator': map.identyfikator, 'generated_chunks': map.generated_chunks, 'players': map.players, 'saved_chunks': map.chunks_saved_into_files}
        with open(f"maps/{map.name}/map_info.json", 'w') as f:
            json.dump(map_file, f)

    def responding_to_connection(self):
        p = 1
        while True:
            id = [p]
            conn, addr = self.server.accept()
            print("Connected to:", addr)
            conn.send(pickle.dumps(id))
            self.players[p] = {}
            self.players[p]['name'] = pickle.loads(conn.recv(262144))
            start_new_thread(self.threaded_client, (conn, p))
            p += 1




server = Server()
server.initialization()
server.bind(5)
server.responding_to_connection()