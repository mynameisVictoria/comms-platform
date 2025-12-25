import socket

class Sockets:
    def __init__(self):
        self.port = 6767
        self.server_socket = None
        self.client_socket = None
        self.client_address = None

    def make_client_socket(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind(("0.0.0.0", self.port))




