from tkinter import *
from plateau import *
from testserv import *
from queue import Queue
import ast
import threading
import pygame
BG_COLOR = [50,50,50]
FONT_COLOR = [255,255,255]



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

def debugCasePos():                 #* affiche dans la console les coordonnées de la case sur laquelle on clique, fonction de debug uniquement
    x,y = pygame.mouse.get_pos()
    x,y = x//50, y//25
    print(x,y)

def debugCaseValide(oldX,oldY):     #* affiche si la case cliquée est valide pour bouger l'anneau (selon des conditions dont je ne me souviens pas)
    x,y = pygame.mouse.get_pos()
    x,y = x//50, y//25
    diffX = oldX - x
    diffY = oldY - y
    print(diffX,diffY)
    if abs(diffX) == abs(diffY) or abs(diffX)%2 == 0 and abs(diffY) == 0 or abs(diffY)%2 == 0 and abs(diffX) == 0:
        print("valide")
    else:
        print("invalide")


def main():
    pygame.init()
    windowWidth = 600       #* Largeur fenêtre (int)
    windowHeight = 600      #* Hauteur fenêtre (int)
    windowStayOpened = True     #* fait tourner la boucle qui affiche la fenêtre pygame (bool)
    screen = pygame.display.set_mode((windowWidth, windowHeight))
    screen.fill(BG_COLOR)       #* BG_COLOR = variable globale équivalente à une directive de preproc (ah et si on a le moindre point en moins parce-que c'est une variable globale c'est que le full prof sait pas dev hein, c'est du basique là)


    objetPlateau = Plateau(10)      #* instanciation par la classe Plateau, paramètre : taille du plateau
    objetPlateau.plateauInitialisation()    #* définit les cases valides du plateau sur la première dimension du plateau tri-dimensionnel (ouais flemme de m'emmerder avec plusieurs objets, 3 dimensions c'est plus simple)

    estClique = False       #* utile pour la fonction gestionClic uniquement, détermine si le clic est déjà enfoncé lors du passage dans la boucle ou pas(bool)
    tourJoueur = 0          #* détermine le tour du joueur en fonction de la parité du nombre (int)
    anneauEnDeplacement = False     #* détermine si un anneau est en train d'être déplacé (bool)
    positionAnneauX = 0     #* position originale abscisse de l'anneau qui est déplacé (int)
    positionAnneauY = 0     #* position originale ordonnée de l'anneau qui est déplacé (int)

    while windowStayOpened:

        objetPlateau.affichagePlateau(screen)   #* affichage des cases du plateau dans la fenêtre
        objetPlateau.affichagePions(screen)     #* affichage des pions dans la fenêtre

        estClique = gestionClic(estClique)      #* transforme le click hold en toggle 
        if estClique:
            if objetPlateau.get_anneauxPlaces() < 4:    #* si les joueurs n'ont pas encore terminé de placer leurs anneaux
                tourJoueur = objetPlateau.placementAnneaux(tourJoueur)     #* placement des anneaux
            else:
                #$debugCasePos()
                if anneauEnDeplacement:     #* si l'anneau a déjà été transformé en marqueur et qu'on attend la position finale de l'anneau pour le replacer
                    anneauEnDeplacement = objetPlateau.checkLigneDeplacementAnneau(positionAnneauX, positionAnneauY)    #* on vérifie que l'anneau puisse être placé aux nouvelles coordonnées selon les règles du jeu
                    if not anneauEnDeplacement:     #* si anneauEnDeplacement est false c'est que la vérification d'avant est validée, donc on continue, sinon on ne fait rien
                        tourJoueur = objetPlateau.placementAnneaux(tourJoueur)      #* on place l'anneau
                        objetPlateau.retournerMarqueurs(positionAnneauX, positionAnneauY)   #* on retourne les marqueurs du chemin s'il y en a
                else:
                    anneauEnDeplacement, positionAnneauX, positionAnneauY = objetPlateau.selectionAnneaux(tourJoueur)   #* aucun anneau en déplacement donc on transforme l'anneau sélectionné en marqueur pour le déplacement à la boucle suivante

        #?fontColor = [255*((tourJoueur+1)%2),255*((tourJoueur+1)%2),255*((tourJoueur+1)%2)]        #* couleur de la police en fonction du tour du joueur  /!\ Contestable /!\
        tourJoueurTexte = renduTexteTourJoueur(tourJoueur)  #* texte à afficher selon le tour du joueur
        font = pygame.font.SysFont(None, 22)        #* texte à afficher
        img = font.render(tourJoueurTexte, True, FONT_COLOR)    #* blabla chiant de pygame, plus d'infos sur la doc offi
        screen.blit(img, (20, 20))      #* pareil

        for event in pygame.event.get():    #* on récupère les events qui se passent
            if event.type == pygame.QUIT:       #* si l'event est un clic sur la croix de la fenêtre
                windowStayOpened = False        #* on toggle la variable pour arrêter la boucle
        pygame.display.update()         #* on met à jour l'affichage de la fenêtre pour appliquer tous les changements survenus dans l'itération de la boucle
        if estClique: 
            print("\n\n\ntest1_get_plateau")
            print (objetPlateau.get_plateau())
    pygame.quit()       #* une fois en dehors de la boucle, ferme la fenêtre pygame


def mainP2P ():
    queue = Queue()
    if __name__ == "__main__":
        host_name = Server.get_local_ip() #* récupérer hostname pour bind la connexion
        port = 1111 #* definition du port utilisé
        server = Server(host_name, port) #* création de l'instance server
        server.bind() #* bind la connexion avec le port et l'adresse ip
        connection, addr = server.accept_connection() #* accept la connexion du client -> serveur
        #test connection
        message_recu = server.receive_message(connection) #* test de connection
        message = ("Server : Bonjour le serveur est aussi vivant ! :D") #* test de connection
        server.send_message(connection, message) #* test de connection
    
        receive_position_thread = threading.Thread(target=server.receive_position_thread, args=(queue,connection))
        receive_position_thread.start()
    
        pygame.init()
        windowWidth = 600       #* Largeur fenêtre (int)
        windowHeight = 600      #* Hauteur fenêtre (int)
        windowStayOpened = True     #* fait tourner la boucle qui affiche la fenêtre pygame (bool)
        screen = pygame.display.set_mode((windowWidth, windowHeight))
        screen.fill(BG_COLOR)       #* BG_COLOR = variable globale équivalente à une directive de preproc (ah et si on a le moindre point en moins parce-que c'est une variable globale c'est que le full prof sait pas dev hein, c'est du basique là)
    
    
        objetPlateau = Plateau(10)      #* instanciation par la classe Plateau, paramètre : taille du plateau
        objetPlateau.plateauInitialisation()    #* définit les cases valides du plateau sur la première dimension du plateau tri-dimensionnel (ouais flemme de m'emmerder avec plusieurs objets, 3 dimensions c'est plus simple)
    
        estClique = False       #* utile pour la fonction gestionClic uniquement, détermine si le clic est déjà enfoncé lors du passage dans la boucle ou pas(bool)
        tourJoueur = 0          #* détermine le tour du joueur en fonction de la parité du nombre (int)
        anneauEnDeplacement = False     #* détermine si un anneau est en train d'être déplacé (bool)
        positionAnneauX = 0     #* position originale abscisse de l'anneau qui est déplacé (int)
        positionAnneauY = 0     #* position originale ordonnée de l'anneau qui est déplacé (int)
        print ("\ntest envoie liste vite\n")
        server.send_message(connection, str(objetPlateau.plateau)) #* envoie d'une liste vide au client
        server.send_message(connection, str(tourJoueur)) #* envoie du tour par défaut au client
        while windowStayOpened: #* boucle execution pygame
            objetPlateau.affichagePlateau(screen)   #* affichage des cases du plateau dans la fenêtre
            objetPlateau.affichagePions(screen)     #* affichage des pions dans la fenêtre
            estClique = gestionClic(estClique)
    
            #*gestion tour host (envoi data vers client)
            if tourJoueur%2 == 0: #* et que c'est le joueur blanc qui joue
                if estClique: #* si on clique dans la fenetre 
                    if objetPlateau.get_anneauxPlaces() < 4: #* vérif que tous les anneaux sont placés
                        tourJoueur = objetPlateau.placementAnneaux(tourJoueur) #* placements d'anneaux si nécessaire
                        message_plateau = "plateau:" + str(objetPlateau.plateau)
                        server.send_message(connection, message_plateau)#* envoie du tableau après mouvements
                        message_tour = "tour:" + str(tourJoueur)
                        server.send_message(connection, message_tour)#* envoie du tour après mouvements
                        objetPlateau.update_display(screen)
                        pygame.display.update()
                    else:
                        if anneauEnDeplacement:     #* si l'anneau a déjà été transformé en marqueur et qu'on attend la position finale de l'anneau pour le replacer
                            anneauEnDeplacement = objetPlateau.checkLigneDeplacementAnneau(positionAnneauX, positionAnneauY)    #* on vérifie que l'anneau puisse être placé aux nouvelles coordonnées selon les règles du jeu
                            if not anneauEnDeplacement:     #* si anneauEnDeplacement est false c'est que la vérification d'avant est validée, donc on continue, sinon on ne fait rien
                                tourJoueur = objetPlateau.placementAnneaux(tourJoueur)      #* on place l'anneau
                                objetPlateau.retournerMarqueurs(positionAnneauX, positionAnneauY)   #* on retourne les marqueurs du chemin s'il y en a
    
                                message_plateau = "plateau:" + str(objetPlateau.plateau) #* ajout de l'identifiant de la donnée
                                server.send_message(connection, message_plateau)#* envoie du tableau après mouvements
                                message_tour = "tour:" + str(tourJoueur) #* ajout de l'identifiant de la donnée
                                server.send_message(connection, message_tour)#* envoie du tourn après mouvements
                                objetPlateau.update_display(screen)
                                pygame.display.update()
                        else:
                            anneauEnDeplacement, positionAnneauX, positionAnneauY = objetPlateau.selectionAnneaux(tourJoueur)   #* aucun anneau en déplacement donc on transforme l'anneau sélectionné en marqueur pour le déplacement à la boucle suivante
                            message_plateau = "plateau:" + str(objetPlateau.plateau) #* ajout de l'identifiant de la donnée
                            server.send_message(connection, message_plateau)#* envoie du tableau après mouvements
                            message_tour = "tour:" + str(tourJoueur) #* ajout de l'identifiant de la donnée
                            server.send_message(connection, message_tour)#* envoie du tableau après mouvements
                            objetPlateau.update_display(screen)
                            pygame.display.update()               
            #* gestion tour invité (réception data de client->validation->changement->update->sendboard)           
            elif tourJoueur%2 == 1:
                    while not queue.empty(): #* on navige les éléments de la queue
                        element = queue.get() #* récupère les éléments de la queue
                        Pos_x_y = ast.literal_eval(element) #* on transforme la string en liste donc = [x, y]
                        x = Pos_x_y[0] #* affectation de valeur de x
                        y = Pos_x_y[1] #* affectation de valeur de y
                        if objetPlateau.get_anneauxPlaces() < 4:    #* si les joueurs n'ont pas encore terminé de placer leurs anneaux
                            tourJoueur = objetPlateau.placementAnneauxP2P(tourJoueur,x,y) #* placement de l'anneau en fonction de x et y
                            message_plateau = "plateau:" + str(objetPlateau.plateau) #* concatenation pour format lisible
                            server.send_message(connection, message_plateau)#* envoie du tableau après mouvements
                            message_tour = "tour:" + str(tourJoueur) #* concatenation pour format lisible
                            server.send_message(connection, message_tour)#* envoie du tour après mouvements
                            objetPlateau.update_display(screen) #* refresh des list 
                            pygame.display.update()   #* refresh interface
            #?fontColor = [255*((tourJoueur+1)%2),255*((tourJoueur+1)%2),255*((tourJoueur+1)%2)]        #* couleur de la police en fonction du tour du joueur  /!\ Contestable /!\
            tourJoueurTexte = renduTexteTourJoueur(tourJoueur)  #* texte à afficher selon le tour du joueur
            font = pygame.font.SysFont(None, 22)        #* texte à afficher
            img = font.render(tourJoueurTexte, True, FONT_COLOR)    #* blabla chiant de pygame, plus d'infos sur la doc office
            screen.blit(img, (20, 20))      #* pareil
    
            for event in pygame.event.get():    #* on récupère les events qui se passent
                if event.type == pygame.QUIT:       #* si l'event est un clic sur la croix de la fenêtre
                    windowStayOpened = False        #* on toggle la variable pour arrêter la boucle
            pygame.display.update()         #* on met à jour l'affichage de la fenêtre pour appliquer tous les changements survenus dans l'itération de la boucle
        server.connected = False
        pygame.quit()
                    

        
#$ truc temporaire à la con sera remplacé par une interface pygame
try:
    input = 1
    #input = int(input("Enter 1-réseau or 2-local: "))
    if input == 1:
        mainP2P()
    elif input == 2:
        main()
except ValueError:
    print("Error: Invalid input. Please enter 1 or 2.")
