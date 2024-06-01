import socket
import ast
import pygame
import threading
from queue import Queue
from plateau import *
from entrer_ip import *
BG_COLOR = [50,50,50]
FONT_COLOR = [255,255,255]

class Client:
    def __init__(self, host_name, port):
        self.host_name = host_name
        self.port = port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.buf_size = 2048
        self.connected = False

    def connect(self): #* effectue la connection la cible
        self.client_socket.connect((self.host_name, self.port))
        self.connected = True
        print("Connected to server")

    def send_message(self, message): #* envoie les messages via la socket
        self.client_socket.send(message.encode())
        print(f"Sent message: {message}")

    def receive_message(self): #* recoit les message envoyé via la socket
        message = self.client_socket.recv(self.buf_size).decode()
        print(f"Received message: {message}")
        return message

    def close(self): #* close socket connection
        self.client_socket.close()
        print("Connection closed")

    def get_local_ip(): #* return local ipv4 address
        host_name = socket.gethostname()
        local_ip = socket.gethostbyname(host_name)
        return local_ip

    def receive_messages_thread(self, queue): #* ajoute le plateau et le tourjoueur à la queue (utilise dans le thread)
        while self.connected:
            message_recu = self.receive_message()
            if message_recu.startswith("plateau:"):
                #plateau_recu = ast.literal_eval(message_recu[8:])
                queue.put(str(message_recu))
                print("un plateau à été ajouté à la queue")
            elif message_recu.startswith("tour:"):
                #tourJoueur = int(message_recu[5:])
                queue.put(str(message_recu))
                print("un tour à été ajouté à la queue")

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
    

def yinshclient (ip):
    queue = Queue()
    if __name__ == "__main__":
        #host_name = Client.get_local_ip() #$ récupérer hostname pour bind la connexion (à changer pour un input)
        host_name = ip #$ récupérer hostname pour bind la connexion (à changer pour un input)
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
        tourJoueur = int(tour)          #* détermine le tour du joueur en fonction de la parité du nombre (int)

        receive_messages_thread = threading.Thread(target=client.receive_messages_thread, args=(queue,)) #* liaison du process à faire tourner sur le thread
        receive_messages_thread.start() #* démarrage du thread
        
        pygame.init()
        windowWidth = 600       #* Largeur fenêtre (int)
        windowHeight = 600      #* Hauteur fenêtre (int)
        windowStayOpened = True     #* fait tourner la boucle qui affiche la fenêtre pygame (bool)
        screen = pygame.display.set_mode((windowWidth, windowHeight))
        screen.fill(BG_COLOR)       #* BG_COLOR = variable globale équivalente à une directive de preproc (ah et si on a le moindre point en moins parce-que c'est une variable globale c'est que le full prof sait pas dev hein, c'est du basique là)
        estClique = False       #* utile pour la fonction gestionClic uniquement, détermine si le clic est déjà enfoncé lors du passage dans la boucle ou pas(bool)
        marqueursAlignes = False
        marqueursAlignesListe = list()
        tourJoueurAlignement = 0
        pointsBlancs = 0
        pointsNoirs = 0
        tourJoueur = 0
        anneauEnDeplacement = False     #* détermine si un anneau est en train d'être déplacé (bool)
        positionAnneauX = 0     #* position originale abscisse de l'anneau qui est déplacé (int)
        positionAnneauY = 0     #* position originale ordonnée de l'anneau qui est déplacé (int)
        modeJeu = 1         #* 3 = partie normale, 1 = partie Blitz

        first_exec = True 
        while windowStayOpened: #* boucle execution pygame
            anneauxBlancs, anneauxNoirs = objetPlateau.get_anneaux_nombre()
            pointsBlancs = 5 - anneauxBlancs
            pointsNoirs = 5 - anneauxNoirs

            if pointsBlancs == modeJeu or pointsNoirs == modeJeu:
                windowStayOpened = False

            objetPlateau.affichagePlateau(screen)   #* affichage des cases du plateau dans la fenêtre
            objetPlateau.affichagePions(screen)     #* affichage des pions dans la fenêtre
            estClique = gestionClic(estClique)

            #*gestion tour host (envoi data vers client)
            if (tourJoueur+tourJoueurAlignement)%2 == 1: #* et que c'est le joueur blanc qui joue
                #if not marqueursAlignes:
                    if estClique: #* si on clique dans la fenetre 
                        if objetPlateau.get_anneauxPlaces() < 2: #* vérif que tous les anneaux sont placés
                            tourJoueur = objetPlateau.placementAnneaux(tourJoueur) #* placements d'anneaux si nécessaire
                            
                            message_plateau = "plateau:" + str(objetPlateau.plateau) #* ajout de l'identifiant de la donnée
                            client.send_message(message_plateau)#* envoie du tableau après mouvements
                            message_tour = "tour:" + str(tourJoueur+tourJoueurAlignement) #* ajout de l'identifiant de la donnée
                            client.send_message(message_tour)#* envoie du tableau après mouvements
                            objetPlateau.update_display(screen)
                            pygame.display.update()   
                        else:
                            if anneauEnDeplacement:     #* si l'anneau a déjà été transformé en marqueur et qu'on attend la position finale de l'anneau pour le replacer
                                anneauEnDeplacement = objetPlateau.checkdeplacementAnneau()    #* on vérifie que l'anneau puisse être placé aux nouvelles coordonnées selon les règles du jeu
                                if not anneauEnDeplacement:     #* si anneauEnDeplacement est false c'est que la vérification d'avant est validée, donc on continue, sinon on ne fait rien
                                    tourJoueur = objetPlateau.placementAnneaux(tourJoueur)      #* on place l'anneau
                                    objetPlateau.retournerMarqueurs(positionAnneauX, positionAnneauY)   #* on retourne les marqueurs du chemin s'il y en a
                                    objetPlateau.del_possibles_moves()
                                    marqueursAlignes, marqueursAlignesListe = objetPlateau.checkAlignementMarqueurs()
                                    if marqueursAlignes == True:
                                        if objetPlateau.get_case_pion() == "A" and (tourJoueur+tourJoueurAlignement)%2 == 1 or objetPlateau.get_case_pion() == "a" and (tourJoueur+tourJoueurAlignement)%2 == 0:
                                            if objetPlateau.get_case_pion() == "A":
                                                pointsBlancs += 1
                                            if objetPlateau.get_case_pion() == "a":
                                                pointsNoirs += 1
                                        print("point blancs: ", pointsBlancs)
                                        print("point noir: ", pointsNoirs)
                                        objetPlateau.set_case_pion(0)
                                        objetPlateau.suppressionMarqueursAlignement(marqueursAlignesListe)                                                     
                                        #print(marqueursAlignesListe)
                                        #if objetPlateau.plateau[1][marqueursAlignesListe[0][0]][marqueursAlignesListe[0][1]] == "m" and tourJoueur%2 == 1:    #* check si le premier marqueur de la liste est de la même couleur que le joueur actuellement en train de jouer, si c'est le cas il faut que le joueur soit à nouveau en train de jouer au prochain tour
                                        #    tourJoueurAlignement = -1
                                        #elif objetPlateau.plateau[1][marqueursAlignesListe[0][0]][marqueursAlignesListe[0][1]] == "M" and tourJoueur%2 == 0:
                                        #    tourJoueurAlignement = -1
                                    message_plateau = "plateau:" + str(objetPlateau.plateau) #* ajout de l'identifiant de la donnée
                                    client.send_message(message_plateau)#* envoie du tableau après mouvements
                                    message_tour = "tour:" + str(tourJoueur+tourJoueurAlignement) #* ajout de l'identifiant de la donnée
                                    client.send_message(message_tour)#* envoie du tableau après mouvements
                                    objetPlateau.update_display(screen)
                                    pygame.display.update()   
                            else:
                                x,y = pygame.mouse.get_pos()
                                x,y = x//50, y//25
                                if objetPlateau.checkifpossibles_moves(x,y):
                                        anneauEnDeplacement, positionAnneauX, positionAnneauY = objetPlateau.selectionAnneaux(tourJoueur)   #* aucun anneau en déplacement donc on transforme l'anneau sélectionné en marqueur pour le déplacement à la boucle suivante
                                        objetPlateau.gen_all_previews(positionAnneauX,positionAnneauY)
                                        if not anneauEnDeplacement:
                                            objetPlateau.del_possibles_moves()
                                        
                                        message_plateau = "plateau:" + str(objetPlateau.plateau) #* ajout de l'identifiant de la donnée
                                        client.send_message(message_plateau)#* envoie du tableau après mouvements
                                        message_tour = "tour:" + str(tourJoueur+tourJoueurAlignement) #* ajout de l'identifiant de la donnée
                                        client.send_message(message_tour)#* envoie du tableau après mouvements
                                        objetPlateau.gen_all_previews(positionAnneauX,positionAnneauY)
                                        objetPlateau.update_display(screen)
                                        pygame.display.update()   
                #* gestion tour invité (réception data de client->validation->changement->update->sendboard)           
                #else:
                #    if estClique:
                #        if objetPlateau.get_case_pion() == "A" and (tourJoueur+tourJoueurAlignement)%2 == 1 or objetPlateau.get_case_pion() == "a" and (tourJoueur+tourJoueurAlignement)%2 == 0:
                #            if objetPlateau.get_case_pion() == "A":
                #                pointsBlancs += 1
                #            if objetPlateau.get_case_pion() == "a":
                #                pointsNoirs += 1
                #            objetPlateau.set_case_pion(0)
                #            objetPlateau.suppressionMarqueursAlignement(marqueursAlignesListe)
                #            marqueursAlignes = False
                #            tourJoueurAlignement = 0
                #            message_plateau = "plateau:" + str(objetPlateau.plateau) #* ajout de l'identifiant de la donnée
                #            client.send_message(message_plateau)#* envoie du tableau après mouvements
                #            message_tour = "tour:" + str(tourJoueur+tourJoueurAlignement) #* ajout de l'identifiant de la donnée
                #            client.send_message(message_tour)#* envoie du tableau après mouvements
                #            objetPlateau.update_display(screen)
                #            pygame.display.update()

            elif (tourJoueur+tourJoueurAlignement)%2 == 0:
                    while not queue.empty(): #* itère les éléments de la queue
                        element = queue.get() #* récupère les éléments de la queue
                        if element.startswith("plateau:"): #* check l'identificant pour savoir de quelle donnée il s'agit
                            message_recu = element
                            plateau_recu = ast.literal_eval(message_recu[8:]) #* formate la data retire l'identifiant
                            objetPlateau.plateau = plateau_recu
                        elif element.startswith("tour:"): #* check l'identificant pour savoir de quelle donnée il s'agit
                            message_recu = element
                            tourJoueur = int(message_recu[5:]) #* formate la data retire l'identifiant
                        objetPlateau.del_possibles_moves()
                        #marqueursAlignes, marqueursAlignesListe = objetPlateau.checkAlignementMarqueurs()
                        #if marqueursAlignes == True:
                        #    print(marqueursAlignesListe)
                        #    if objetPlateau.plateau[1][marqueursAlignesListe[0][0]][marqueursAlignesListe[0][1]] == "m" and tourJoueur%2 == 1:    #* check si le premier marqueur de la liste est de la même couleur que le joueur actuellement en train de jouer, si c'est le cas il faut que le joueur soit à nouveau en train de jouer au prochain tour
                        #        tourJoueurAlignement = -1
                        #    elif objetPlateau.plateau[1][marqueursAlignesListe[0][0]][marqueursAlignesListe[0][1]] == "M" and tourJoueur%2 == 0:
                        #        tourJoueurAlignement = -1
                        objetPlateau.update_display(screen) #* affiche le plateau avec un refresh
                        pygame.display.update() #* refresh de l'interface pour afficher les changement si dessus                             

            tourJoueurTexte = renduTexteTourJoueur(tourJoueur)  #* texte à afficher selon le tour du joueur
            font = pygame.font.SysFont(None, 22)        #* texte à afficher
            img = font.render(tourJoueurTexte, True, FONT_COLOR)    #* blabla chiant de pygame, plus d'infos sur la doc office
            txt = font.render("Vous jouez les noirs", True, FONT_COLOR)    #* blabla chiant de pygame, plus d'infos sur la doc office
            screen.blit(img, (20, 20))      #* pareil
            screen.blit(txt, (375, 20))      #* pareil
            for event in pygame.event.get():    #* on récupère les events qui se passent
                if event.type == pygame.QUIT:       #* si l'event est un clic sur la croix de la fenêtre
                    client.close()
                    receive_messages_thread.join()  #* fermeture du thread
                    windowStayOpened = False        #* on toggle la variable pour arrêter la boucle
                    client.connected = False
            pygame.display.update()         #* on met à jour l'affichage de la fenêtre pour appliquer tous les changements survenus dans l'itération de la boucle
    
        client.connected = False
    if pointsNoirs > pointsBlancs:
        print("Les noirs remportent la victoire !")
    else:
        print("Les blancs remportent la victoire !")
    pygame.quit()

def main ():
    #ip = ''
    #ip = interface()

    ip = Client.get_local_ip() #* obtenir ip local pour test 
    yinshclient(ip)


main()