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
    

def gestionClic(estClique):             #* renvoie true uniquement si le clic de la souris est enfoncé alors qu'il ne l'était pas à la boucle précédente
    if pygame.mouse.get_pressed()[0]:
        if estClique == False:
            if pygame.mouse.get_pressed()[0]:
                return True
    else:
        return False

def renduTexteTourJoueur(tourJoueur):       #* renvoie le texte à afficher selon le tour du joueur
    if tourJoueur%2 == 0:
        return "Aux Blancs de jouer"
    else:
        return "Aux Noirs de jouer"
    
def main ():
    if __name__ == "__main__":
        host_name = Client.get_local_ip()
        port = 1111
        client = Client(host_name, port)
        client.connect()
        client.send_message("Bonjour le client est vivant ! :)")
        message_recu = client.receive_message()
        plateau_recu = ast.literal_eval(message_recu)
        tour = client.receive_message()
        #print(plateau_recu)
        #print(type(message_recu))
        #print(message_recu)
        #print("test1\n")
        #print(plateau_recu[1])
        objetPlateau = Plateau(10)
        objetPlateau.plateau = plateau_recu

        pygame.init()
        windowWidth = 600       #* Largeur fenêtre (int)
        windowHeight = 600      #* Hauteur fenêtre (int)
        windowStayOpened = True     #* fait tourner la boucle qui affiche la fenêtre pygame (bool)
        screen = pygame.display.set_mode((windowWidth, windowHeight))
        screen.fill(BG_COLOR)       #* BG_COLOR = variable globale équivalente à une directive de preproc (ah et si on a le moindre point en moins parce-que c'est une variable globale c'est que le full prof sait pas dev hein, c'est du basique là)
        estClique = False       #* utile pour la fonction gestionClic uniquement, détermine si le clic est déjà enfoncé lors du passage dans la boucle ou pas(bool)
        tourJoueur = int(tour)          #* détermine le tour du joueur en fonction de la parité du nombre (int)
        anneauEnDeplacement = False     #* détermine si un anneau est en train d'être déplacé (bool)
        positionAnneauX = 0     #* position originale abscisse de l'anneau qui est déplacé (int)
        positionAnneauY = 0     #* position originale ordonnée de l'anneau qui est déplacé (int)
        while windowStayOpened:
            objetPlateau.affichagePlateau(screen)
            objetPlateau.affichagePions(screen)

            estClique = gestionClic(estClique)      #* transforme le click hold en toggle 
            if estClique:
                if objetPlateau.get_anneauxPlaces() < 4:    #* si les joueurs n'ont pas encore terminé de placer leurs anneaux
                    x,y = pygame.mouse.get_pos()
                    x,y = x//50, y//25
                    client.send_message(str([x, y]))  #* Envoyer les positions x et y dans une liste

            #?fontColor = [255*((tourJoueur+1)%2),255*((tourJoueur+1)%2),255*((tourJoueur+1)%2)]        #* couleur de la police en fonction du tour du joueur  /!\ Contestable /!\
            tourJoueurTexte = renduTexteTourJoueur(tourJoueur)  #* texte à afficher selon le tour du joueur
            font = pygame.font.SysFont(None, 22)        #* texte à afficher
            img = font.render(tourJoueurTexte, True, FONT_COLOR)    #* blabla chiant de pygame, plus d'infos sur la doc offi
            screen.blit(img, (20, 20))      #* pareil
            for event in pygame.event.get():    #* on récupère les events qui se passent
                if event.type == pygame.QUIT:       #* si l'event est un clic sur la croix de la fenêtre
                    windowStayOpened = False
            pygame.display.update() 
    client.close()
main()