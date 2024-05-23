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
        print(f"Received message: {message}")
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
        host_name = Client.get_local_ip() #$ récupérer hostname pour bind la connexion (à changer pour un input)
        port = 1111 #* definition du port utilisé
        client = Client(host_name, port) #* création de l'instance server
        client.connect() #* connextion à l'adresse donné
        client.send_message("Bonjour le client est vivant ! :)") #* test de connection
        client.receive_message() #* test de connection


        message_recu = client.receive_message() #* réception d'une grille vide
        plateau_recu = ast.literal_eval(message_recu)
        tour = client.receive_message() #* réception du tour
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
        first_exec = True 
        while windowStayOpened:
            objetPlateau.affichagePlateau(screen)  #* affiche le plateau
            objetPlateau.affichagePions(screen) #* affiche les pions si ils sont présent
            if first_exec == True: #* permet d'afficher la grille lors de l'ouverture
                pygame.display.update() #* update l'interface afin d'affciher le plateau recu
                first_exec = False #* ajout de cette variable pour concel l'auto refresh permanent
            if tourJoueur%2 == 0: #* si le joueur à jouer n'est pas l'invité on receptionne le plateau lors qde chaque mouvements
                print ("test") 
                tour = client.receive_message() #*réception tour après tour du joueur blanc
                message_recu = client.receive_message() #* réception du plateau après le tour du joueur blanc
                plateau_recu = ast.literal_eval(message_recu) #* converti le tableau qui est en str en list
                objetPlateau.plateau = plateau_recu #* affectation du tableau à la classe Plateau              
                print ("test1")
                tourJoueur = int(tour) #* affectation et conversion du tourjoueur
                print ("test3")
                objetPlateau.affichagePlateau(screen) #* affichage du nouveau plateau après le tour du joueur blanc
                objetPlateau.affichagePions(screen) #* affichage des pions après le tour du joueur blanc
                pygame.display.update() #* refresh de l'interface pour afficher les changement si dessus
                print ("test4")
            else :
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