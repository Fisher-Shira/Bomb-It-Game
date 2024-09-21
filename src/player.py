from socket import socket, AF_INET, SOCK_STREAM
from src.color import Color

ENCODING = 'utf-8'
IP = '127.0.0.1'
PORT = 1729
NUM_HEARTS = 3


class Player:
    def __init__(self):
        self.p_socket = None
        self.color = None
        self.column = Color.start_column["pink"]  # x position
        self.raw = Color.start_raw["pink"]  # y position
        self.hearts = NUM_HEARTS
        self.direction = "d"  # d=down, u=up, r=right, l=left
        self.bombs = 0  # how many bombs put

    def reset(self):
        self.color = None
        self.column = Color.start_column["pink"]  # x position
        self.raw = Color.start_raw["pink"]  # y position
        self.hearts = NUM_HEARTS
        self.direction = "d"  # d=down, u=up, r=right, l=left
        self.bombs = 0  # how many bombs put

    def connect_play(self):
        # connect to the sever
        self.p_socket = socket(AF_INET, SOCK_STREAM)
        self.p_socket.connect((IP, PORT))

    def set_color(self, color):
        # Set color, start position
        self.color = color
        self.column = Color.start_column[color]
        self.raw = Color.start_raw[color]

    def send_act(self, act):
        # Send act to the server
        self.p_socket.send(str(act).encode(ENCODING))

    def get_act(self):
        # Get act from the server
        length = self.p_socket.recv(2)
        if (length == ''):
            return None
        data = self.p_socket.recv(int(length.decode(ENCODING)
                                      )).decode(ENCODING)
        return data
