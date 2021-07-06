import socket
import threading
import string
import json
from random import choices
from socket import AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR
from core import get_location, is_winner, is_tie

class Server:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.buff_size = 2048

        self.rooms = {}
        self.players = {}
        self.layout = [
            ['-', '-', '-'],
            ['-', '-', '-'],
            ['-', '-', '-']
        ]
        self.current = 'X'

        self.server = socket.socket(AF_INET, SOCK_STREAM)
        self.server.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.server.bind((self.host, self.port))
        self.init_server()
    
    @staticmethod
    def generate_room_id():
        return ''.join(choices(string.ascii_uppercase + string.digits, k=5))

    def init_room(self, data, conn):
        username, room_id = data['username'], data['room_id']
        self.players[username] = conn

        if data['room_id'] in self.rooms.keys():
            if len(self.rooms[room_id]) >= 2:
                print("room full")
            else:
                self.rooms[room_id].append({
                    'username': username,
                    'score': 0,
                    'alias': 'O' if self.rooms[room_id][0]['alias'] == 'X' else 'X'
                })
                self.room_boardcast(room_id, 'room_joined')
        else:
            self.rooms[room_id] = []
            data = {
                'username': username,
                'alias': self.current,
                'score': 0
            }
            self.rooms[room_id].append(data)

    def handle_gameplay(self, conn):
        while True:
            data = json.loads(conn.recv(self.buff_size).decode())
            if data['type'] == 'move_played':
                if data['player_data']['alias'] == self.current:
                    x, y, x_pos, y_pos = data['layout_data']
                    if self.layout[x-1][y-1] == '-':
                        self.layout[x-1][y-1] = data['player_data']['alias']
                        if is_winner(self.layout, self.current):
                            self.room_boardcast(data['room_id'], 'has_won', self.current)
                            self.layout = [['-', '-', '-'], ['-', '-', '-'], ['-', '-', '-']]
                        elif is_tie(self.layout):
                            self.room_boardcast(data['room_id'], 'is_tie')
                            self.layout = [['-', '-', '-'], ['-', '-', '-'], ['-', '-', '-']]
                        else:
                            self.current = 'O' if self.current == 'X' else 'X'

                            layout_update = {
                                'type': 'layout_update',
                                'current': self.current,
                                'move_by': data['player_data'],
                                'moved_to': data['layout_data']
                            }
                            self.room_boardcast(data['room_id'], 'layout_update', layout_update)

    def room_boardcast(self, room_id, boardcast_type, data_to_emit=None):
        for data in self.rooms[room_id]:
            conn = self.players[data['username']]
            if boardcast_type == 'room_joined':
                conn.send(json.dumps({
                    'type': 'room_joined',
                    'current': self.current,
                    'data': self.rooms[room_id]
                }).encode())
            elif boardcast_type == 'layout_update':
                conn.send(json.dumps(data_to_emit).encode())
            elif boardcast_type == 'has_won':
                conn.send(json.dumps({
                    'type': 'has_won',
                    'winner': data_to_emit
                }).encode())
            elif boardcast_type == 'is_tie':
                conn.send(json.dumps({
                    'type': 'is_tie'
                }).encode())
    
    def init_server(self):
        self.server.listen(10)
        print('listening ...')
        while True:
            conn, addr = self.server.accept()
            data = json.loads(conn.recv(self.buff_size).decode())
            if data['type'] == 'init':
                self.init_room(data, conn)
            threading.Thread(target=self.handle_gameplay, args=(conn,), daemon=True).start()

server = Server('localhost', 8000)
