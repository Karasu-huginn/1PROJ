from tkinter import *
from plateau import *
from testserv import *
from menu import *
from jouer_sur_ce_pc import *
from normal_blitz import *
from interface_win import *
from queue import Queue
import subprocess
import ast
import threading
import pygame

BG_COLOR = [50, 50, 50]
FONT_COLOR = [255, 255, 255]
BUTTON_BG_COLOR = [98, 114, 127]
BUTTON_BORDER_COLOR = [0, 0, 0]



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

def draw_button(screen, text, position, size=(300, 50), bg_color=BUTTON_BG_COLOR, border_color=BUTTON_BORDER_COLOR):
    font = pygame.font.SysFont(None, 30)
    rect = pygame.Rect(position, size)
    pygame.draw.rect(screen, border_color, rect, border_radius=12)
    inner_rect = rect.inflate(-4, -4)
    pygame.draw.rect(screen, bg_color, inner_rect, border_radius=10)
    img = font.render(text, True, [0, 0, 0])
    screen.blit(img, (rect.centerx - img.get_width() // 2, rect.centery - img.get_height() // 2))
    return rect

def draw_button_save(screen, text, position, size=(140, 50), bg_color=BUTTON_BG_COLOR, border_color=BUTTON_BORDER_COLOR):
    font = pygame.font.SysFont(None, 30)
    rect = pygame.Rect(position, size)
    pygame.draw.rect(screen, border_color, rect, border_radius=12)
    inner_rect = rect.inflate(-4, -4)
    pygame.draw.rect(screen, bg_color, inner_rect, border_radius=10)
    img = font.render(text, True, [0, 0, 0])
    screen.blit(img, (rect.centerx - img.get_width() // 2, rect.centery - img.get_height() // 2))
    return rect

def draw_button_charger(screen, text, position, size=(140, 50), bg_color=BUTTON_BG_COLOR, border_color=BUTTON_BORDER_COLOR):
    font = pygame.font.SysFont(None, 30)
    rect = pygame.Rect(position, size)
    pygame.draw.rect(screen, border_color, rect, border_radius=12)
    inner_rect = rect.inflate(-4, -4)
    pygame.draw.rect(screen, bg_color, inner_rect, border_radius=10)
    img = font.render(text, True, [0, 0, 0])
    screen.blit(img, (rect.centerx - img.get_width() // 2, rect.centery - img.get_height() // 2))
    return rect

def draw_text_top_right(screen, text):
    font = pygame.font.SysFont(None, 40)
    img = font.render(text, True, FONT_COLOR)
    screen.blit(img, (screen.get_width() - img.get_width() - 10, 10))


def main(modeJeu):
    pygame.init()
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)  # Définit le mode de la fenêtre en plein écran
    screen.fill(BG_COLOR)
    windowStayOpened = True     #* fait tourner la boucle qui affiche la fenêtre pygame (bool)
   
    # Charger l'image yinsh.png
    yinsh_img = pygame.image.load("yinsh.png")
    new_width, new_height = 600, 200
    yinsh_img = pygame.transform.scale(yinsh_img, (new_width, new_height))
    yinsh_img_rect = yinsh_img.get_rect()
    yinsh_img_rect.midtop = (screen.get_width() // 1.6, 20)  # Positionne l'image au centre en haut

    boardImage = pygame.image.load("yinsh_board.png")
    boardImage = pygame.transform.scale(boardImage, (535,500))
    boardImage_rect = boardImage.get_rect()
    boardImage_rect.topleft = (5,0)  # Positionne l'image dans le coin

    

    objetPlateau = Plateau(10)      #* instanciation par la classe Plateau, paramètre : taille du plateau
    objetPlateau.plateauInitialisation()    #* définit les cases valides du plateau sur la première dimension du plateau tri-dimensionnel (ouais flemme de m'emmerder avec plusieurs objets, 3 dimensions c'est plus simple)

    estClique = False       #* utile pour la fonction gestionClic uniquement, détermine si le clic est déjà enfoncé lors du passage dans la boucle ou pas(bool)
    tourJoueur = 0          #* détermine le tour du joueur en fonction de la parité du nombre (int)
    anneauEnDeplacement = False     #* détermine si un anneau est en train d'être déplacé (bool)
    positionAnneauX = 0     #* position originale abscisse de l'anneau qui est déplacé (int)
    positionAnneauY = 0     #* position originale ordonnée de l'anneau qui est déplacé (int)
    pointsBlancs = 0
    pointsNoirs = 0
    marqueursAlignes = False
    marqueursAlignesListe = list()
    tourJoueurAlignement = 0

    # Configuration de la zone de texte défilante
    text_scroll_surface = pygame.Surface((screen.get_width() - 200, 400))
    text_scroll_surface.fill(BG_COLOR)
    scroll_y = 0
    scroll_speed = 20  # Augmenter la vitesse de défilement

    while windowStayOpened:
        screen.fill(BG_COLOR)  # Nettoie l'écran avant chaque nouveau rendu

        # Affiche l'image au centre en haut
        screen.blit(yinsh_img, yinsh_img_rect)

        if pointsBlancs == modeJeu or pointsNoirs == modeJeu:
            windowStayOpened = False

        screen.blit(boardImage, boardImage_rect)    #* affichage du plateau dans l'interface
        objetPlateau.affichagePions(screen)     #* affichage des pions dans la fenêtre

        estClique = gestionClic(estClique)      #* transforme le click hold en toggle 
        if not marqueursAlignes:
            if estClique:                       #! valeur à changer avant rendu final !
                if objetPlateau.get_anneauxPlaces() < 10:    #* si les joueurs n'ont pas encore terminé de placer leurs anneaux
                    tourJoueur = objetPlateau.placementAnneaux(tourJoueur)     #* placement des anneaux
                else:
                    if anneauEnDeplacement:     #* si l'anneau a déjà été transformé en m arqueur et qu'on attend la position finale de l'anneau pour le replacer
                        anneauEnDeplacement = objetPlateau.checkdeplacementAnneau()    #* on vérifie que l'anneau puisse être placé aux nouvelles coordonnées selon les règles du jeu
                        if not anneauEnDeplacement:     #* si anneauEnDeplacement est false c'est que la vérification d'avant est validée, donc on continue, sinon on ne fait rien
                            tourJoueur = objetPlateau.placementAnneaux(tourJoueur)      #* on place l'anneau
                            objetPlateau.retournerMarqueurs(positionAnneauX, positionAnneauY)   #* on retourne les marqueurs du chemin s'il y en a
                            objetPlateau.del_possibles_moves()
                            marqueursAlignes, marqueursAlignesListe = objetPlateau.checkAlignementMarqueurs()
                            if marqueursAlignes == True:
                                print(marqueursAlignesListe)
                                if objetPlateau.plateau[1][marqueursAlignesListe[0][0]][marqueursAlignesListe[0][1]] == "m" and tourJoueur%2 == 1:    #* check si le premier marqueur de la liste est de la même couleur que le joueur actuellement en train de jouer, si c'est le cas il faut que le joueur soit à nouveau en train de jouer au prochain tour
                                    tourJoueurAlignement = -1
                                elif objetPlateau.plateau[1][marqueursAlignesListe[0][0]][marqueursAlignesListe[0][1]] == "M" and tourJoueur%2 == 0:
                                    tourJoueurAlignement = -1
                    else:
                        x,y = pygame.mouse.get_pos()
                        x,y = x//50, y//25
                        if 0 <= y < objetPlateau.taillePlateauX and 0 <= x < objetPlateau.taillePlateauY:
                            if objetPlateau.plateau[1][x][y] == "a" or objetPlateau.plateau[1][x][y] == "A":
                                objetPlateau.gen_all_previews(x,y)
                                if objetPlateau.has_possibles_moves():
                                    anneauEnDeplacement, positionAnneauX, positionAnneauY = objetPlateau.selectionAnneaux(tourJoueur)   #* aucun anneau en déplacement donc on transforme l'anneau sélectionné en marqueur pour le déplacement à la boucle suivante    
                                    objetPlateau.gen_all_previews(positionAnneauX,positionAnneauY)
                                    if not anneauEnDeplacement:
                                        objetPlateau.del_possibles_moves()
        else:
            if estClique:
                if objetPlateau.get_case_pion() == "A" and (tourJoueur+tourJoueurAlignement)%2 == 1 or objetPlateau.get_case_pion() == "a" and (tourJoueur+tourJoueurAlignement)%2 == 0:
                    if objetPlateau.get_case_pion() == "A":
                        pointsBlancs += 1
                    if objetPlateau.get_case_pion() == "a":
                        pointsNoirs += 1
                    objetPlateau.set_case_pion(0)
                    objetPlateau.suppressionMarqueursAlignement(marqueursAlignesListe)
                    marqueursAlignes = False
                    tourJoueurAlignement = 0

        tourJoueurTexte = renduTexteTourJoueur(tourJoueur+tourJoueurAlignement)
        font = pygame.font.SysFont(None, 39)
        img = font.render(tourJoueurTexte, True, FONT_COLOR)
        text_x = (screen.get_width() - img.get_width()) // 2  # Centrer horizontalement
        text_y = yinsh_img_rect.bottom + 80
        screen.blit(img, (text_x, text_y))

        tourJoueurTexte = renduTexteTourJoueur(tourJoueur+tourJoueurAlignement)
        font = pygame.font.SysFont(None, 39)
        img = font.render(tourJoueurTexte, True, FONT_COLOR)
        text_x = (screen.get_width() - img.get_width()) // 2  # Centrer horizontalement
        text_y = yinsh_img_rect.bottom + 150
        screen.blit(img, (text_x, text_y))

    
        # Dessiner les boutons
        button_x = screen.get_width() - 350
        button_charger = screen.get_width() - 190
        reset_button_rect = draw_button(screen, "Reset", (button_x, 340))
        quit_button_rect = draw_button(screen, "Quitter", (button_x, 415))
        save_button_rect = draw_button_save(screen, "Sauvegarder", (button_x, 265))
        load_button_rect = draw_button_charger(screen, "Charger", (button_charger, 265))

        # Dessiner la ligne de séparation
        line_y = 540  # Position verticale de la ligne (juste au-dessus du texte défilant)
        pygame.draw.line(screen, BUTTON_BORDER_COLOR, (100, line_y), (screen.get_width() - 100, line_y), 2)

        custom_text = "Règles du jeu YINSH"
        custom_font = pygame.font.SysFont(None, 50)
        custom_text_img = custom_font.render(custom_text, True, FONT_COLOR)
        custom_text_x = (screen.get_width() - custom_text_img.get_width()) // 2
        custom_text_pos = (custom_text_x, 580)  # Position du texte (x, y)
        screen.blit(custom_text_img, custom_text_pos)


        # Gérer le texte défilant
        text_scroll_surface.fill(BG_COLOR)
        text_to_display = [
            "But du jeu : Créer une rangée de cinq anneaux de votre couleur",
            "Le jeu se joue sur un plateau avec 5 anneaux noirs et 5 anneaux blancs ainsi que des pions de la même couleur.",
            "",
            "Chaque joueur commence la partie avec 5 marqueurs de sa couleur, qu'il place aux intersections",
            "",
            "À tour de rôle, chaque joueur effectue les actions suivantes :",
            "1. Prendre un marqueur de sa réserve",
            "2. Déplacer un anneau en respectant les règles de déplacement",
            "3. Retourner les pions sur les intersections sautées (si applicable)",
            "4. Vérifier si une rangée de cinq anneaux ou pions yinsh de sa couleur a été formée",
            "5. Retirer les anneaux ou pions yinsh de la rangée formée et les remettre dans la réserve",
            "6. Retirer un anneau de sa couleur du jeu",
            "",
            "Fin du Jeu : Le jeu se termine dès qu'un joueur a réussi à aligner cinq anneaux ou pions yinsh de sa couleur. Ce joueur est alors déclaré vainqueur.",
        ]

        line_height = 30
        font = pygame.font.SysFont(None, 28)
        for i, line in enumerate(text_to_display):
            line_img = font.render(line, True, FONT_COLOR)
            line_x = (text_scroll_surface.get_width() - line_img.get_width()) // 2  # Centrer horizontalement
            text_scroll_surface.blit(line_img, (line_x, i * line_height - scroll_y))

        screen.blit(text_scroll_surface, (100, screen.get_height() - 430))  # Ajuster la position verticale

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return  # Quitte la fonction main()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:  # Si la touche Echap est pressée
                pygame.quit()
                return  # Quitte la fonction main()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Si le bouton gauche de la souris est cliqué
                mouse_pos = event.pos
                if save_button_rect.collidepoint(mouse_pos):
                    subprocess.run(["python", "sauvegarder.py"])
                elif load_button_rect.collidepoint(mouse_pos):
                    subprocess.run(["python", "charger.py"])
                elif reset_button_rect.collidepoint(mouse_pos):
                    for i in range(len(objetPlateau.plateau[1])):
                        for u in range(len(objetPlateau.plateau[1][i])):
                            if objetPlateau.plateau[1][i][u] != 0:
                                objetPlateau.plateau [1][i][u] = 0
                                tourJoueur = 0          #* détermine le tour du joueur en fonction de la parité du nombre (int)
                                objetPlateau.anneauxPlaces = 0
                                anneauEnDeplacement = False     #* détermine si un anneau est en train d'être déplacé (bool)
                                positionAnneauX = 0     #* position originale abscisse de l'anneau qui est déplacé (int)
                                positionAnneauY = 0     #* position originale ordonnée de l'anneau qui est déplacé (int)
                                pointsBlancs = 0
                                pointsNoirs = 0
                                marqueursAlignes = False
                                marqueursAlignesListe = list()
                                tourJoueurAlignement = 0
                elif quit_button_rect.collidepoint(mouse_pos):
                    subprocess.run(["python", "quitter.py"])
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4:  # Scroll up
                    scroll_y = max(scroll_y - scroll_speed, 0)
                elif event.button == 5:  # Scroll down
                    scroll_y = min(scroll_y + scroll_speed, len(text_to_display) * line_height - text_scroll_surface.get_height())
        pygame.display.update()         #* on met à jour l'affichage de la fenêtre pour appliquer tous les changements survenus dans l'itération de la boucle
    if pointsNoirs > pointsBlancs:
        win("Les noirs remportent la victoire !")
    else:
        win("Les blancs remportent la victoire !")
    #todo proposition recommencer partie
    pygame.quit()       #* une fois en dehors de la boucle, ferme la fenêtre pygame

















def mainP2P (modeJeu):
    queue = Queue()
    host_name = Server.get_local_ip() #* récupérer hostname pour bind la connexion
    port = 1111 #* definition du port utilisé
    server = Server(host_name, port) #* création de l'instance server
    valid = True
    #server.bind() #* bind la connexion avec le port et l'adresse ip

    #receive_connection_thread = threading.Thread(target=server.accept_connection(), args=()) #* liaison du process à faire tourner sur le thread
    #receive_connection_thread.start() #* démarrage du thread
#
    #while not server.connected: 
    #    ip = Server.get_local_ip()
    #    server.interfaceP2Phost(ip)

    connection, addr, valid = server.bind_and_accept(host_name) #* accept la connexion du client -> serveur
    #test connection
    message_recu = server.receive_message(connection) #* test de connection
    message = ("Server : Bonjour le serveur est aussi vivant ! :D") #* test de connection
    server.send_message(connection, message) #* test de connection

    
    pygame.init()
    screen = pygame.display.set_mode((0, 0))  # Définit le mode de la fenêtre en plein écran
    screen.fill(BG_COLOR)
    windowStayOpened = True     #* fait tourner la boucle qui affiche la fenêtre pygame (bool)

    # Charger l'image yinsh.png
    yinsh_img = pygame.image.load("yinsh.png")
    new_width, new_height = 600, 200
    yinsh_img = pygame.transform.scale(yinsh_img, (new_width, new_height))
    yinsh_img_rect = yinsh_img.get_rect()
    yinsh_img_rect.midtop = (screen.get_width() // 1.6, 20)  # Positionne l'image au centre en haut

    boardImage = pygame.image.load("yinsh_board.png")
    boardImage = pygame.transform.scale(boardImage, (535,500))
    boardImage_rect = boardImage.get_rect()
    boardImage_rect.topleft = (5,0)  # Positionne l'image dans le coin

    objetPlateau = Plateau(10)      #* instanciation par la classe Plateau, paramètre : taille du plateau
    objetPlateau.plateauInitialisation()    #* définit les cases valides du plateau sur la première dimension du plateau tri-dimensionnel (ouais flemme de m'emmerder avec plusieurs objets, 3 dimensions c'est plus simple)

    estClique = False       #* utile pour la fonction gestionClic uniquement, détermine si le clic est déjà enfoncé lors du passage dans la boucle ou pas(bool)
    pointsBlancs = 0
    pointsNoirs = 0
    tourJoueur = 0          #* détermine le tour du joueur en fonction de la parité du nombre (int)
    anneauEnDeplacement = False     #* détermine si un anneau est en train d'être déplacé (bool)
    positionAnneauX = 0     #* position originale abscisse de l'anneau qui est déplacé (int)
    positionAnneauY = 0     #* position originale ordonnée de l'anneau qui est déplacé (int)
    marqueursAlignes = False
    marqueursAlignesListe = list()
    tourJoueurAlignement = 0
    anneauxBlancs = 0
    anneauxNoirs = 0

    # Configuration de la zone de texte défilante
    text_scroll_surface = pygame.Surface((screen.get_width() - 200, 400))
    text_scroll_surface.fill(BG_COLOR)
    scroll_y = 0
    scroll_speed = 20  # Augmenter la vitesse de défilement

    server.send_message(connection, str(objetPlateau.plateau)) #* envoie d'une liste vide au client
    server.send_message(connection, str(tourJoueur)) #* envoie du tour par défaut au client
    receive_messages_thread = threading.Thread(target=server.receive_messages_thread, args=(queue,connection)) #* liaison du process à faire tourner sur le thread
    receive_messages_thread.start() #* démarrage du thread

    tempTicks = 0

    while windowStayOpened: #* boucle execution pygame


        screen.fill(BG_COLOR)
        screen.blit(yinsh_img, yinsh_img_rect)
        screen.blit(boardImage, boardImage_rect)
        if objetPlateau.get_anneauxPlaces() > 5 and anneauEnDeplacement == False:
            anneauxBlancs, anneauxNoirs = objetPlateau.get_anneaux_nombre()
            pointsBlancs = 5 - anneauxBlancs
            pointsNoirs = 5 - anneauxNoirs
        if tempTicks < 500:
            tempTicks += 1
        else:
            tempTicks = 0
            print("AnneauxBlancs : ", anneauxBlancs)
            print("pointsBlancs :", pointsBlancs)
            print("AnneauxNoirs : ", anneauxNoirs)
            print("pointsNoirs :", pointsNoirs)
        if pointsBlancs == modeJeu or pointsNoirs == modeJeu:
            windowStayOpened = False
        
        screen.blit(boardImage, boardImage_rect)    #* affichage du plateau dans l'interface
        objetPlateau.affichagePions(screen)     #* affichage des pions dans la fenêtre
        estClique = gestionClic(estClique)

        #*gestion tour host (envoi data vers client)
        if (tourJoueur+tourJoueurAlignement)%2 == 0: #* et que c'est le joueur blanc qui joue
            #if not marqueursAlignes:
                if estClique: #* si on clique dans la fenetre 
                    if objetPlateau.get_anneauxPlaces() < 5: #* vérif que tous les anneaux sont placés
                        tourJoueur = objetPlateau.placementAnneaux(tourJoueur) #* placements d'anneaux si nécessaire
                        message_plateau = "plateau:" + str(objetPlateau.plateau) #* ajout de l'identifiant de la donnée
                        server.send_message(connection, message_plateau)#* envoie du tableau après mouvements
                        message_tour = "tour:" + str(tourJoueur+tourJoueurAlignement) #* ajout de l'identifiant de la donnée
                        server.send_message(connection, message_tour)#* envoie du tableau après mouvements
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
                                server.send_message(connection, message_plateau)#* envoie du tableau après mouvements
                                message_tour = "tour:" + str(tourJoueur+tourJoueurAlignement) #* ajout de l'identifiant de la donnée
                                server.send_message(connection, message_tour)#* envoie du tableau après mouvements
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
                                    server.send_message(connection,message_plateau)#* envoie du tableau après mouvements
                                    message_tour = "tour:" + str(tourJoueur+tourJoueurAlignement) #* ajout de l'identifiant de la donnée
                                    server.send_message(connection,message_tour)#* envoie du tableau après mouvements
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
            #            if not local:
            #                message_plateau = "plateau:" + str(objetPlateau.plateau) #* ajout de l'identifiant de la donnée
            #                server.send_message(connection, message_plateau)#* envoie du tableau après mouvements
            #                message_tour = "tour:" + str(tourJoueur+tourJoueurAlignement) #* ajout de l'identifiant de la donnée
            #                server.send_message(connection, message_tour)#* envoie du tableau après mouvements
            #                objetPlateau.update_display(screen)
            #                pygame.display.update()



        elif (tourJoueur+tourJoueurAlignement)%2 == 1:
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

        tourJoueurTexte = "Vous avez les Blancs"
        font = pygame.font.SysFont(None, 39)
        img = font.render(tourJoueurTexte, True, FONT_COLOR)
        text_x = (screen.get_width() - img.get_width()) // 2  # Centrer horizontalement
        text_y = yinsh_img_rect.bottom + 80
        screen.blit(img, (text_x, text_y))

        tourJoueurTexte = renduTexteTourJoueur(tourJoueur)
        font = pygame.font.SysFont(None, 39)
        img = font.render(tourJoueurTexte, True, FONT_COLOR)
        text_x = (screen.get_width() - img.get_width()) // 2  # Centrer horizontalement
        text_y = yinsh_img_rect.bottom + 150
        screen.blit(img, (text_x, text_y))

    
        # Dessiner les boutons
        button_x = screen.get_width() - 350
        button_xx = screen.get_width() - 700
        button_charger = screen.get_width() - 190
        reset_button_rect = draw_button(screen, "Reset", (button_xx, 450))
        quit_button_rect = draw_button(screen, "Quitter", (button_x, 450))

        # Dessiner la ligne de séparation
        line_y = 540  # Position verticale de la ligne (juste au-dessus du texte défilant)
        pygame.draw.line(screen, BUTTON_BORDER_COLOR, (100, line_y), (screen.get_width() - 100, line_y), 2)

        custom_text = "Règles du jeu YINSH"
        custom_font = pygame.font.SysFont(None, 50)
        custom_text_img = custom_font.render(custom_text, True, FONT_COLOR)
        custom_text_x = (screen.get_width() - custom_text_img.get_width()) // 2
        custom_text_pos = (custom_text_x, 580)  # Position du texte (x, y)
        screen.blit(custom_text_img, custom_text_pos)


        # Gérer le texte défilant
        text_scroll_surface.fill(BG_COLOR)
        text_to_display = [
            "But du jeu : Créer une rangée de cinq anneaux de votre couleur",
            "Le jeu se joue sur un plateau avec 5 anneaux noirs et 5 anneaux blancs ainsi que des pions de la même couleur.",
            "",
            "Chaque joueur commence la partie avec 5 marqueurs de sa couleur, qu'il place aux intersections",
            "",
            "À tour de rôle, chaque joueur effectue les actions suivantes :",
            "1. Prendre un marqueur de sa réserve",
            "2. Déplacer un anneau en respectant les règles de déplacement",
            "3. Retourner les pions sur les intersections sautées (si applicable)",
            "4. Vérifier si une rangée de cinq anneaux ou pions yinsh de sa couleur a été formée",
            "5. Retirer les anneaux ou pions yinsh de la rangée formée et les remettre dans la réserve",
            "6. Retirer un anneau de sa couleur du jeu",
            "",
            "Fin du Jeu : Le jeu se termine dès qu'un joueur a réussi à aligner cinq anneaux ou pions yinsh de sa couleur. Ce joueur est alors déclaré vainqueur.",
        ]

        line_height = 30
        font = pygame.font.SysFont(None, 28)
        for i, line in enumerate(text_to_display):
            line_img = font.render(line, True, FONT_COLOR)
            line_x = (text_scroll_surface.get_width() - line_img.get_width()) // 2  # Centrer horizontalement
            text_scroll_surface.blit(line_img, (line_x, i * line_height - scroll_y))

        screen.blit(text_scroll_surface, (100, screen.get_height() - 430))  # Ajuster la position verticale

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return  # Quitte la fonction main()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:  # Si la touche Echap est pressée
                pygame.quit()
                return  # Quitte la fonction main()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Si le bouton gauche de la souris est cliqué
                mouse_pos = event.pos
                if reset_button_rect.collidepoint(mouse_pos):
                    for i in range(len(objetPlateau.plateau[1])):
                        for u in range(len(objetPlateau.plateau[1][i])):
                            if objetPlateau.plateau[1][i][u] != 0:
                                objetPlateau.plateau [1][i][u] = 0
                                tourJoueur = 0          #* détermine le tour du joueur en fonction de la parité du nombre (int)
                                objetPlateau.anneauxPlaces = 0
                                anneauEnDeplacement = False     #* détermine si un anneau est en train d'être déplacé (bool)
                                positionAnneauX = 0     #* position originale abscisse de l'anneau qui est déplacé (int)
                                positionAnneauY = 0     #* position originale ordonnée de l'anneau qui est déplacé (int)
                                pointsBlancs = 0
                                pointsNoirs = 0
                                marqueursAlignes = False
                                marqueursAlignesListe = list()
                                tourJoueurAlignement = 0
                elif quit_button_rect.collidepoint(mouse_pos):
                    subprocess.run(["python", "quitter.py"])
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Si le bouton gauche de la souris est cliqué
                mouse_pos = event.pos
                if reset_button_rect.collidepoint(mouse_pos):
                    subprocess.run(["python", "reset.py"])
                elif quit_button_rect.collidepoint(mouse_pos):
                    subprocess.run(["python", "quitter.py"])
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4:  # Scroll up
                    scroll_y = max(scroll_y - scroll_speed, 0)
                elif event.button == 5:  # Scroll down
                    scroll_y = min(scroll_y + scroll_speed, len(text_to_display) * line_height - text_scroll_surface.get_height())
        pygame.display.update()         #* on met à jour l'affichage de la fenêtre pour appliquer tous les changements survenus dans l'itération de la boucle
    if pointsNoirs > pointsBlancs:
        win("Les noirs remportent la victoire !")
    else:
        win("Les blancs remportent la victoire !")
    #todo proposition recommencer partie
    #pygame.quit()       #* une fois en dehors de la boucle, ferme la fenêtre pygame











def mainIA(modeJeu):

    pygame.init()
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)  # Définit le mode de la fenêtre en plein écran
    screen.fill(BG_COLOR)
    windowStayOpened = True     #* fait tourner la boucle qui affiche la fenêtre pygame (bool)

    boardImage = pygame.image.load("yinsh_board.png")
    boardImage = pygame.transform.scale(boardImage, (535,500))
    boardImage_rect = boardImage.get_rect()
    boardImage_rect.topleft = (5,0)  # Positionne l'image dans le coin

    objetPlateau = Plateau(10)      #* instanciation par la classe Plateau, paramètre : taille du plateau
    objetPlateau.plateauInitialisation()    #* définit les cases valides du plateau sur la première dimension du plateau tri-dimensionnel (ouais flemme de m'emmerder avec plusieurs objets, 3 dimensions c'est plus simple)
    estClique = False       #* utile pour la fonction gestionClic uniquement, détermine si le clic est déjà enfoncé lors du passage dans la boucle ou pas(bool)
    tourJoueur = 0          #* détermine le tour du joueur en fonction de la parité du nombre (int)
    anneauEnDeplacement = False     #* détermine si un anneau est en train d'être déplacé (bool)
    positionAnneauX = 0     #* position originale abscisse de l'anneau qui est déplacé (int)
    positionAnneauY = 0     #* position originale ordonnée de l'anneau qui est déplacé (int)
    pointsBlancs = 0
    pointsNoirs = 0
    marqueursAlignes = False
    marqueursAlignesListe = list()
    tourJoueurAlignement = 0

    # Configuration de la zone de texte défilante
    text_scroll_surface = pygame.Surface((screen.get_width() - 200, 400))
    text_scroll_surface.fill(BG_COLOR)
    scroll_y = 0
    scroll_speed = 20  # Augmenter la vitesse de défilement

    while windowStayOpened:
        if pointsBlancs == modeJeu or pointsNoirs == modeJeu:
            windowStayOpened = False
        screen.blit(boardImage, boardImage_rect)    #* affichage du plateau dans l'interface
        objetPlateau.affichagePions(screen)     #* affichage des pions dans la fenêtre
        estClique = gestionClic(estClique)      #* transforme le click hold en toggle 
        if (tourJoueur+tourJoueurAlignement) % 2 == 0:
            if not marqueursAlignes:
                if estClique:                       #! valeur à changer avant rendu final !
                    if objetPlateau.get_anneauxPlaces() < 10:    #* si les joueurs n'ont pas encore terminé de placer leurs anneaux
                        tourJoueur = objetPlateau.placementAnneaux(tourJoueur)     #* placement des anneaux
                    else:
                        if anneauEnDeplacement:     #* si l'anneau a déjà été transformé en m arqueur et qu'on attend la position finale de l'anneau pour le replacer
                            anneauEnDeplacement = objetPlateau.checkdeplacementAnneau()    #* on vérifie que l'anneau puisse être placé aux nouvelles coordonnées selon les règles du jeu
                            if not anneauEnDeplacement:     #* si anneauEnDeplacement est false c'est que la vérification d'avant est validée, donc on continue, sinon on ne fait rien
                                tourJoueur = objetPlateau.placementAnneaux(tourJoueur)      #* on place l'anneau
                                objetPlateau.retournerMarqueurs(positionAnneauX, positionAnneauY)   #* on retourne les marqueurs du chemin s'il y en a
                                objetPlateau.del_possibles_moves()
                                marqueursAlignes, marqueursAlignesListe = objetPlateau.checkAlignementMarqueurs()
                                if marqueursAlignes == True:
                                    if objetPlateau.plateau[1][marqueursAlignesListe[0][0]][marqueursAlignesListe[0][1]] == "m" and tourJoueur%2 == 0:    #* check si le premier marqueur de la liste est de la même couleur que le joueur actuellement en train de jouer, si c'est le cas il faut que le joueur soit à nouveau en train de jouer au prochain tour
                                        tourJoueurAlignement = -1
                                    elif objetPlateau.plateau[1][marqueursAlignesListe[0][0]][marqueursAlignesListe[0][1]] == "M" and tourJoueur%2 == 1:
                                        tourJoueurAlignement = -1
                        else:
                            x,y = pygame.mouse.get_pos()
                            x,y = x//50, y//25
                            if 0 <= y < objetPlateau.taillePlateauX and 0 <= x < objetPlateau.taillePlateauY:
                                if objetPlateau.plateau[1][x][y] == "a" or objetPlateau.plateau[1][x][y] == "A":
                                    objetPlateau.gen_all_previews(x,y)
                                    if objetPlateau.has_possibles_moves():
                                        anneauEnDeplacement, positionAnneauX, positionAnneauY = objetPlateau.selectionAnneaux(tourJoueur)   #* aucun anneau en déplacement donc on transforme l'anneau sélectionné en marqueur pour le déplacement à la boucle suivante    
                                        objetPlateau.gen_all_previews(positionAnneauX,positionAnneauY)
                                        if not anneauEnDeplacement:
                                            objetPlateau.del_possibles_moves()
            else:
                if estClique:
                    if objetPlateau.get_case_pion() == "A" and (tourJoueur+tourJoueurAlignement)%2 == 0:
                        if objetPlateau.get_case_pion() == "A":
                            pointsBlancs += 1
                        if objetPlateau.get_case_pion() == "a":
                            pointsNoirs += 1
                        objetPlateau.set_case_pion(0)
                        objetPlateau.suppressionMarqueursAlignement(marqueursAlignesListe)
                        marqueursAlignes = False
                        tourJoueurAlignement = 0
        else:
            if not marqueursAlignes:
                if objetPlateau.get_anneauxPlaces() < 10:
                    x, y = objetPlateau.gen_rand_pos_x_y_empty()
                    tourJoueur = objetPlateau.placementAnneauxIA(tourJoueur,x,y)
                else:
                    if anneauEnDeplacement:
                        x, y = objetPlateau.gen_rand_pos_x_y_previsu()
                        anneauEnDeplacement = objetPlateau.checkdeplacementAnneauIA(x,y)
                        if not anneauEnDeplacement:
                            tourJoueur = objetPlateau.placementAnneauxIA(tourJoueur,x,y)
                            objetPlateau.retournerMarqueursIA(positionAnneauX, positionAnneauY,x,y)
                            objetPlateau.del_possibles_moves()
                            marqueursAlignes, marqueursAlignesListe = objetPlateau.checkAlignementMarqueurs()
                            if marqueursAlignes == True:
                                if objetPlateau.plateau[1][marqueursAlignesListe[0][0]][marqueursAlignesListe[0][1]] == "m" and tourJoueur%2 == 0:    #* check si le premier marqueur de la liste est de la même couleur que le joueur actuellement en train de jouer, si c'est le cas il faut que le joueur soit à nouveau en train de jouer au prochain tour
                                    tourJoueurAlignement = -1
                                elif objetPlateau.plateau[1][marqueursAlignesListe[0][0]][marqueursAlignesListe[0][1]] == "M" and tourJoueur%2 == 1:
                                    tourJoueurAlignement = -1
                    else:
                        x, y = objetPlateau.gen_rand_pos_x_y_Anneaux()
                        if objetPlateau.checkifpossibles_moves:
                            anneauEnDeplacement , positionAnneauX, positionAnneauY = objetPlateau.selectionAnneauxIA(tourJoueur,x,y)
                            objetPlateau.gen_all_previews(positionAnneauX,positionAnneauY)
                            if not anneauEnDeplacement:
                                objetPlateau.del_possibles_moves()
            else:
                x, y = objetPlateau.gen_rand_pos_x_y_Anneaux()
                if objetPlateau.get_pion(x,y) == "a" and (tourJoueur+tourJoueurAlignement)%2 == 1:
                    pointsNoirs += 1
                    objetPlateau.set_pion(x,y,0)
                    objetPlateau.suppressionMarqueursAlignement(marqueursAlignesListe)
                    marqueursAlignes = False
                    tourJoueurAlignement = 0
            

        # Dessiner les boutons
        button_x = screen.get_width() - 350
        button_xx = screen.get_width() - 700
        button_charger = screen.get_width() - 190
        reset_button_rect = draw_button(screen, "Reset", (button_xx, 450))
        quit_button_rect = draw_button(screen, "Quitter", (button_x, 450))

        # Dessiner la ligne de séparation
        line_y = 540  # Position verticale de la ligne (juste au-dessus du texte défilant)
        pygame.draw.line(screen, BUTTON_BORDER_COLOR, (100, line_y), (screen.get_width() - 100, line_y), 2)

        custom_text = "Règles du jeu YINSH"
        custom_font = pygame.font.SysFont(None, 40)
        custom_text_img = custom_font.render(custom_text, True, FONT_COLOR)
        custom_text_x = (screen.get_width() - custom_text_img.get_width()) // 2
        custom_text_pos = (custom_text_x, 580)  # Position du texte (x, y)
        screen.blit(custom_text_img, custom_text_pos)

        # Dessiner le texte "Vous jouez contre une IA" dans le coin supérieur droit
        opponent_text = "Vous jouez contre une IA"
        opponent_font = pygame.font.SysFont(None, 70)
        opponent_text_img = opponent_font.render(opponent_text, True, FONT_COLOR)
        opponent_text_x = screen.get_width() - opponent_text_img.get_width() - 600
        opponent_text_pos = (opponent_text_x, 240)
        screen.blit(opponent_text_img, opponent_text_pos)

        # Gérer le texte défilant
        text_scroll_surface.fill(BG_COLOR)
        text_to_display = [
            "But du jeu : Créer une rangée de cinq anneaux de votre couleur",
            "Le jeu se joue sur un plateau avec 5 anneaux noirs et 5 anneaux blancs ainsi que des pions de la même couleur.",
            "",
            "Chaque joueur commence la partie avec 5 marqueurs de sa couleur, qu'il place aux intersections",
            "",
            "À tour de rôle, chaque joueur effectue les actions suivantes :",
            "1. Prendre un marqueur de sa réserve",
            "2. Déplacer un anneau en respectant les règles de déplacement",
            "3. Retourner les pions sur les intersections sautées (si applicable)",
            "4. Vérifier si une rangée de cinq anneaux ou pions yinsh de sa couleur a été formée",
            "5. Retirer les anneaux ou pions yinsh de la rangée formée et les remettre dans la réserve",
            "6. Retirer un anneau de sa couleur du jeu",
            "",
            "Fin du Jeu : Le jeu se termine dès qu'un joueur a réussi à aligner cinq anneaux ou pions yinsh de sa couleur. Ce joueur est alors déclaré vainqueur.",
        ]

        line_height = 30
        font = pygame.font.SysFont(None, 28)
        for i, line in enumerate(text_to_display):
            line_img = font.render(line, True, FONT_COLOR)
            line_x = (text_scroll_surface.get_width() - line_img.get_width()) // 2  # Centrer horizontalement
            text_scroll_surface.blit(line_img, (line_x, i * line_height - scroll_y))

        screen.blit(text_scroll_surface, (100, screen.get_height() - 430))  # Ajuster la position verticale
  

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return  # Quitte la fonction main()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:  # Si la touche Echap est pressée
                pygame.quit()
                return  # Quitte la fonction main()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Si le bouton gauche de la souris est cliqué
                mouse_pos = event.pos
                if reset_button_rect.collidepoint(mouse_pos):
                    for i in range(len(objetPlateau.plateau[1])):
                        for u in range(len(objetPlateau.plateau[1][i])):
                            if objetPlateau.plateau[1][i][u] != 0:
                                objetPlateau.plateau [1][i][u] = 0
                                tourJoueur = 0          #* détermine le tour du joueur en fonction de la parité du nombre (int)
                                objetPlateau.anneauxPlaces = 0
                                anneauEnDeplacement = False     #* détermine si un anneau est en train d'être déplacé (bool)
                                positionAnneauX = 0     #* position originale abscisse de l'anneau qui est déplacé (int)
                                positionAnneauY = 0     #* position originale ordonnée de l'anneau qui est déplacé (int)
                                pointsBlancs = 0
                                pointsNoirs = 0
                                marqueursAlignes = False
                                marqueursAlignesListe = list()
                                tourJoueurAlignement = 0


                elif quit_button_rect.collidepoint(mouse_pos):
                    subprocess.run(["python", "quitter.py"])
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4:  # Scroll up
                    scroll_y = max(scroll_y - scroll_speed, 0)
                elif event.button == 5:  # Scroll down
                    scroll_y = min(scroll_y + scroll_speed, len(text_to_display) * line_height - text_scroll_surface.get_height())
        pygame.display.update()         #* on met à jour l'affichage de la fenêtre pour appliquer tous les changements survenus dans l'itération de la boucle
    if pointsNoirs > pointsBlancs:
        win("Les noirs remportent la victoire !")
    else:
        win("Les blancs remportent la victoire !")
    #todo proposition recommencer partie
    pygame.quit()       #* une fois en dehors de la boucle, ferme la fenêtre pygame
                    

        
#$ truc temporaire à la con sera remplacé par une interface pygame
#try:
#    input = 1
#    #input = int(input("Enter 1-réseau or 2-local: "))
#    if input == 1:
#        mainP2P()
#    elif input == 2:
#        main()
#    elif input == 3:
#        mainIA()
#except ValueError:
#    print("Error: Invalid input. Please enter 1 or 2.")

inlocal = False
while True:
    value = menu()
    if value == 1:
        #réseau
        value2 = normal_or_blitz()
        if value2 == 1:
            #normal
            mainP2P(3)
        elif value2 == 2:
            #blitz
            mainP2P(1)
    elif value == 2:
        #local
        inlocal = True
        while inlocal:
            value1 = localplay()
            if value1 == 1:
                #jouer à 2
                value2 = normal_or_blitz()
                if value2 == 1:
                    #normal
                    main(3)
                elif value2 == 2:
                    #blitz
                    main(1)#todo à adapter
            elif value1 == 2:
                #jouer contre ia
                value2 = normal_or_blitz()
                if value2 == 1:
                    #normal
                    mainIA(3)
                elif value2 == 2:
                    #blitz
                    mainIA(1)#todo à adapter
                elif value1 == 3:
                    continue
            else:
                break

