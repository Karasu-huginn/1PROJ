import socket
from plateau import *
from queue import Queue
BUFF_SIZE = 2048

class Server:
    def __init__(self, host_name, port):
        self.host_name = host_name
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.buf_size = 2048
        self.connected = False

    def bind(self):
        self.server_socket.bind((self.host_name, self.port))
        self.server_socket.listen()
        print(f"Server listening on {self.host_name}:{self.port}")

    def accept_connection(self):
        connection, addr = self.server_socket.accept()
        print(f"Connected to client : {addr}")
        self.connected = True
        return connection, addr

    def receive_message(self, connection):
        message = connection.recv(self.buf_size).decode()
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
                
    def receive_position_thread(self, queue, connection): #* ajoute x et y à la queue (utilise dans le thread)
        while self.connected:
            message_recu = self.receive_message(connection)
            queue.put(message_recu)
            print("une pos x et y à été ajouté à la queue")

    def data_sending (self,plateau,connection,tourJoueur):
        message_plateau = "plateau:" + str(plateau) #* ajout de l'identifiant de la donnée
        self.send_message(connection, message_plateau)#* envoie du tableau après mouvements
        message_tour = "tour:" + str(tourJoueur) #* ajout de l'identifiant de la donnée
        self.send_message(connection, message_tour)#* envoie du tourn après mouvements