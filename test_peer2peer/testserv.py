import socket
from plateau import *
BUFF_SIZE = 2048

class Server:
    def __init__(self, host_name, port):
        self.host_name = host_name
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def bind(self):
        self.server_socket.bind((self.host_name, self.port))
        self.server_socket.listen()
        print(f"Server listening on {self.host_name}:{self.port}")

    def accept_connection(self):
        connection, addr = self.server_socket.accept()
        print(f"Connected to client : {addr}")
        return connection, addr

    def receive_message(self, connection):
        message = connection.recv(BUFF_SIZE).decode()
        print(f"Received message: {message}")
        return message

    def send_message(self, connection, message):
        connection.send(message.encode())
        print(f"Sent message: {message}")

    def close(self, connection):
        connection.close()
        print("Connection closed")

    def get_local_ip():
        host_name = socket.gethostname()
        local_ip = socket.gethostbyname(host_name)
        return local_ip

