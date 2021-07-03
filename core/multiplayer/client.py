import socket, json
from socket import AF_INET, SOCK_STREAM

class Client:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.buff_size = 2048
        self.server = socket.socket(AF_INET, SOCK_STREAM)
        self.server.connect((self.host, self.port))
    
    def connect(self, data):
        self.server.send(json.dumps(data).encode())

    def played_move(self, data):
        data = json.dumps(data).encode()
        self.server.send(data)
    
    def check_for_player(self):
        while True:
            data = json.loads(self.server.recv(self.buff_size).decode())
            if data:
                return data
