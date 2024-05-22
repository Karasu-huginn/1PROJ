import socket
import ast
import pygame
from plateau import *
BG_COLOR = [50,50,50]
FONT_COLOR = [255,255,255]

class Client:
    def __init__(self, host_name, port):
        self.host_name = host_name
        self.port = port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.buf_size = 2048

    def connect(self):
        self.client_socket.connect((self.host_name, self.port))
        print("Connected to server")

    def send_message(self, message):
        self.client_socket.send(message.encode())
        print(f"Sent message: {message}")

    def receive_message(self):
        message = self.client_socket.recv(self.buf_size).decode()
        #print(f"Received message: {message}")
        return message

    def close(self):
        self.client_socket.close()
        print("Connection closed")

    def get_local_ip():
        host_name = socket.gethostname()
        local_ip = socket.gethostbyname(host_name)
        return local_ip
    def main ():
        if __name__ == "__main__":
            host_name = Client.get_local_ip()
            port = 1111
            client = Client(host_name, port)
            client.connect()
            client.send_message("Bonjour le client est vivant ! :)")
            message_recu = client.receive_message()
            plateau_recu = ast.literal_eval(message_recu)
            #print(plateau_recu)
            #print(type(message_recu))
            #print(message_recu)
            #print("test1\n")
            #print(plateau_recu[1])


            objetPlateau = Plateau(10)
            objetPlateau.plateau = plateau_recu
            print(type(objetPlateau.plateau))
            print(objetPlateau.plateau)
            pygame.init()
            windowWidth = 600       #* Largeur fenêtre (int)
            windowHeight = 600      #* Hauteur fenêtre (int)
            windowStayOpened = True     #* fait tourner la boucle qui affiche la fenêtre pygame (bool)
            screen = pygame.display.set_mode((windowWidth, windowHeight))
            screen.fill(BG_COLOR)       #* BG_COLOR = variable globale équivalente à une directive de preproc (ah et si on a le moindre point en moins parce-que c'est une variable globale c'est que le full prof sait pas dev hein, c'est du basique là)

            while windowStayOpened:
                objetPlateau.affichagePlateau(screen)
                objetPlateau.affichagePions(screen)
                for event in pygame.event.get():    #* on récupère les events qui se passent
                    if event.type == pygame.QUIT:       #* si l'event est un clic sur la croix de la fenêtre
                        windowStayOpened = False
                pygame.display.update() 
        client.close()
Client.main()