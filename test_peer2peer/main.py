from tkinter import *
from plateau import *
from plateau import *
from testserv import *
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
    host_name = Server.get_local_ip()
    port = 1111
    server = Server(host_name, port)
    server.bind()
    connection, addr = server.accept_connection()
    #test connection
    message_recu = server.receive_message(connection)
    message = ("Server : Bonjour le serveur est aussi vivant ! :D")
    server.send_message(connection, message)
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
    server.send_message(connection, str(objetPlateau.plateau))
    server.send_message(connection, str(tourJoueur))
    while windowStayOpened:
        objetPlateau.affichagePlateau(screen)   #* affichage des cases du plateau dans la fenêtre
        objetPlateau.affichagePions(screen)     #* affichage des pions dans la fenêtre
        #plateau ="[[[0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0], [0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0], [0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0], [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1], [0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0], [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1], [0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0], [0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0], [0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0]], [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 'A', 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]]"
        estClique = gestionClic(estClique)
        if estClique:
            if tourJoueur%2 == 0: #les blancs jouent
                if objetPlateau.get_anneauxPlaces() < 4:
                    tourJoueur = objetPlateau.placementAnneaux(tourJoueur)
                    print ("\nenvoie liste après premier anneaux")
                    server.send_message(connection, str(tourJoueur))
                    server.send_message(connection,str(objetPlateau.plateau))
                else:
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
        #if estClique: 
        #    print("\n\n\ntest1_get_plateau je suis la \n\n\n")
        #    print (objetPlateau.get_plateau())
    pygame.quit()
                    

        #while True :
        #    tourJoueur, objetPlateau.plateau , x, y = objetPlateau.placementAnneauxP2P()
        #    Pos = eval(server.receive_message(connection))
        #    x = Pos[0]
        #    y = Pos[1]
        #    #tourdujoueur, plateau, x, y = 

try:
    input = 1
    #input = int(input("Enter 1-réseau or 2-local: "))
    if input == 1:
        mainP2P()
    elif input == 2:
        main()
except ValueError:
    print("Error: Invalid input. Please enter 1 or 2.")
