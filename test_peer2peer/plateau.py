import pygame

class Plateau:
    def __init__(self, taillePlateau):
        self.taillePlateauY = taillePlateau+1
        self.taillePlateauX = int(taillePlateau*2)
        self.plateau = [list(),list()]
        self.pions = list()
        self.anneauxPlaces = 0
        self.marqueurSurChemin = False
        self.anneauSurChemin = False
        self.token = int
    
    def get_taillePlateauY(self):
        return self.taillePlateauY
    
    def get_taillePlateauX(self):
        return self.taillePlateauX
    
    def get_plateau(self):
        return self.plateau
    
    def get_anneauxPlaces(self):
        return self.anneauxPlaces

    def plateauInitialisation(self):
        self.plateau[0] = [[1]*self.taillePlateauX for i in range(self.taillePlateauY)]
        self.plateau[1] = [[0]*self.taillePlateauX for i in range(self.taillePlateauY)]
        for i in range(self.taillePlateauY):
            for u in range(self.taillePlateauX):
                if i == -1:
                    self.plateau[0][i][u] = 0
                else:
                    if i+u > self.taillePlateauX+(self.taillePlateauY//2) or i+u < self.taillePlateauY//2 or i-u > self.taillePlateauY//2 or i-u < (self.taillePlateauY//2)-self.taillePlateauX: #* définition des bordures du plateau
                        self.plateau[0][i][u] = 0
                    if i%2 == u%2: #* suppresion d'une case sur deux pour avoir des cases à alternance triangulaire
                        self.plateau[0][i][u] = 0
                    if u == 0 and i == self.taillePlateauY//2: #* suppression du coin gauche
                        self.plateau[0][i][u] = 0
                    if u == self.taillePlateauX and i == self.taillePlateauY//2: #* suppresion du coin droit
                        self.plateau[0][i][u] = 0
                    if u == self.taillePlateauY//2 and i == 0: #* suppresion du coin haut gauche
                        self.plateau[0][i][u] = 0
                    if u == self.taillePlateauX-(self.taillePlateauY//2) and i == 0: #* suppresion du coin haut droit
                        self.plateau[0][i][u] = 0
                    if u == self.taillePlateauY//2 and i == self.taillePlateauY-1: #* suppresion du coin bas gauche
                        self.plateau[0][i][u] = 0
                    if u == self.taillePlateauX-(self.taillePlateauY//2) and i == self.taillePlateauY-1: #* suppresion du coin bas droit
                        self.plateau[0][i][u] = 0


    def display(self):      #* affiche le plateau en CLI
        for i in range(self.taillePlateauY):
            for u in range(self.taillePlateauX):
                if self.plateau[0][i][u] == 1:
                    if self.plateau[1][i][u] == "A":
                        print("A", end="")
                    elif self.plateau[1][i][u] == "M":
                        print("M", end="")
                    else:
                        print("x", end="")
                if self.plateau[0][i][u] == 0:
                    print(" ", end="")
            print("")

    def affichagePlateau(self, screen):     #* affiche le plateau sur la fenêtre Pygame
        for i in range(len(self.plateau[0])):
            for u in range(len(self.plateau[0][i])):
                if self.plateau[0][i][u] == 1:
                    pygame.draw.rect(screen, (200,200,200), pygame.Rect((i*50, u*25, 50, 25)))
                if self.plateau[0][i][u] == 0:
                    pygame.draw.rect(screen, (50,50,50), pygame.Rect((i*50, u*25, 50, 25)))

    def affichagePions(self, screen):       #* affiche les pions sur la fenêtre Pygame
        for i in range(len(self.plateau[1])):
            for u in range(len(self.plateau[1][i])):
                if self.plateau[1][i][u] == "m":
                    pygame.draw.circle(screen, (0,0,0),(i*50+25,u*25+12), 8)
                elif self.plateau[1][i][u] == "M":
                    pygame.draw.circle(screen, (255,255,255),(i*50+25,u*25+12), 8)
                elif self.plateau[1][i][u] == "a":
                    pygame.draw.circle(screen, (0,0,0),(i*50+25,u*25+12), 12)
                    pygame.draw.circle(screen, (200,200,200),(i*50+25,u*25+12), 8)
                elif self.plateau[1][i][u] == "A":
                    pygame.draw.circle(screen, (255,255,255),(i*50+25,u*25+12), 12)
                    pygame.draw.circle(screen, (200,200,200),(i*50+25,u*25+12), 8)
                elif self.plateau[1][i][u] == "P":
                    pygame.draw.circle(screen, (255,165,0,128),(i*50+25,u*25+12), 12)
                    pygame.draw.circle(screen, (255,140,0,128),(i*50+25,u*25+12), 8) 

                        
    def retournerMarqueurs(self, positionAnneauX, positionAnneauY):     #* retourne tous les marqueurs sur le chemin prit par un anneau
        x,y = pygame.mouse.get_pos()
        x,y = x//50, y//25                                              #* récupère les coordonnées du curseur et les divise par la taille d'une case pour avoir les coordonnées sur le plateau
        diffX = positionAnneauX-x                                       #* nombre de cases entre la position orginale et la nouvelle position de l'anneau
        diffY = positionAnneauY-y
        if abs(diffX) == abs(diffY):                                    #* vérifie que la case sélectionnée est une diagonale de la case originale
            for i in range(1,abs(diffX)):
                loopX = positionAnneauX-i*(diffX//abs(diffX))           #* définit les coordonnées d'une case où retourner le marqueur si présent
                loopY = positionAnneauY-i*(diffY//abs(diffY))
                if self.plateau[1][loopX][loopY] == "m":                #* retourne le marqueur
                    self.plateau[1][loopX][loopY] = "M"
                elif self.plateau[1][loopX][loopY] == "M":
                    self.plateau[1][loopX][loopY] = "m"
        elif abs(diffX)%2 == 0 and abs(diffY) == 0 or abs(diffY)%2 == 0 and abs(diffX) == 0:    #* vérifie que la case sélectionnée est une ligne horizontale ou verticale de la case originale
            for i in range(1,(abs(diffX)+abs(diffY)+1)//2):
                if abs(diffX) == 0:
                    loopX = positionAnneauX
                    loopY = positionAnneauY-i*(diffY//abs(diffY))*2
                    if self.plateau[1][loopX][loopY] == "m":
                        self.plateau[1][loopX][loopY] = "M"
                    elif self.plateau[1][loopX][loopY] == "M":
                        self.plateau[1][loopX][loopY] = "m"
                else:
                    loopX = positionAnneauX-i*(diffX//abs(diffX))*2
                    loopY = positionAnneauY
                    if self.plateau[1][loopX][loopY] == "m":
                        self.plateau[1][loopX][loopY] = "M"
                    elif self.plateau[1][loopX][loopY] == "M":
                        self.plateau[1][loopX][loopY] = "m"



    def retournerMarqueursP2P(self, positionAnneauX, positionAnneauY,x,y):     #* retourne tous les marqueurs sur le chemin prit par un anneau                                        #* récupère les coordonnées du curseur et les divise par la taille d'une case pour avoir les coordonnées sur le plateau
        diffX = positionAnneauX-x                                       #* nombre de cases entre la position orginale et la nouvelle position de l'anneau
        diffY = positionAnneauY-y
        if abs(diffX) == abs(diffY):                                    #* vérifie que la case sélectionnée est une diagonale de la case originale
            for i in range(1,abs(diffX)):
                loopX = positionAnneauX-i*(diffX//abs(diffX))           #* définit les coordonnées d'une case où retourner le marqueur si présent
                loopY = positionAnneauY-i*(diffY//abs(diffY))
                if self.plateau[1][loopX][loopY] == "m":                #* retourne le marqueur
                    self.plateau[1][loopX][loopY] = "M"
                elif self.plateau[1][loopX][loopY] == "M":
                    self.plateau[1][loopX][loopY] = "m"
        elif abs(diffX)%2 == 0 and abs(diffY) == 0 or abs(diffY)%2 == 0 and abs(diffX) == 0:    #* vérifie que la case sélectionnée est une ligne horizontale ou verticale de la case originale
            for i in range(1,(abs(diffX)+abs(diffY)+1)//2):
                if abs(diffX) == 0:
                    loopX = positionAnneauX
                    loopY = positionAnneauY-i*(diffY//abs(diffY))*2
                    if self.plateau[1][loopX][loopY] == "m":
                        self.plateau[1][loopX][loopY] = "M"
                    elif self.plateau[1][loopX][loopY] == "M":
                        self.plateau[1][loopX][loopY] = "m"
                else:
                    loopX = positionAnneauX-i*(diffX//abs(diffX))*2
                    loopY = positionAnneauY
                    if self.plateau[1][loopX][loopY] == "m":
                        self.plateau[1][loopX][loopY] = "M"
                    elif self.plateau[1][loopX][loopY] == "M":
                        self.plateau[1][loopX][loopY] = "m"
                        

    def placementAnneaux(self, tourJoueur):    #* place un anneau où le joueur a cliqué
        x,y = pygame.mouse.get_pos()
        x,y = x//50, y//25
        if self.plateau[0][x][y] == 1:          #* vérifie que la case sélectionnée est une intersection libre
            if self.plateau[1][x][y] == 0 or self.plateau[1][x][y] == "P":  #* vérifie que la case sélectionnée est vide
                if tourJoueur%2 == 0:               #* choisit la couleur en fonction de si tourJoueur est pair ou impair
                    self.plateau[1][x][y] = "A"
                    tourJoueur+=1
                    self.anneauxPlaces+=1
                else:
                    self.plateau[1][x][y] = "a"
                    tourJoueur+=1
                    self.anneauxPlaces+=1
        return tourJoueur
    
    def placementAnneauxP2P(self, tourJoueur, x, y):
        if self.plateau[0][x][y] == 1:
            if self.plateau[1][x][y] == 0:  #* vérifie que la case sélectionnée est vide
                if tourJoueur%2 == 0:               #* choisit la couleur en fonction de si tourJoueur est pair ou impair
                    self.plateau[1][x][y] = "A"
                    tourJoueur+=1
                    self.anneauxPlaces+=1
                else:
                    self.plateau[1][x][y] = "a"
                    tourJoueur+=1
                    self.anneauxPlaces+=1
        return tourJoueur
 
    def selectionAnneaux(self, tourJoueur):     #* sélectionne un anneau à déplacer
        x,y = pygame.mouse.get_pos()
        x,y = x//50, y//25
        if self.plateau[1][x][y] == chr((tourJoueur%2)*32+65):  #* vérifie que le pion sélectionné correspond à un anneau de la couleur du joueur (si tourJoueur est pair, 32 n'est pas ajouté à 65 et reste "m", sinon le chr() le passe en majuscule selon son code ASCII)
            if tourJoueur%2 == 0:
                self.plateau[1][x][y] = "M"                     #* remplace l'anneau par un marqueur en vue de la suite du tour
            else:
                self.plateau[1][x][y] = "m"
            return True, x, y
        else:
            return False, 0, 0    
    
    def selectionAnneauxP2P(self, tourJoueur, x, y):     #* sélectionne un anneau à déplacer
        if self.plateau[1][x][y] == chr((tourJoueur%2)*32+65):  #* vérifie que le pion sélectionné correspond à un anneau de la couleur du joueur (si tourJoueur est pair, 32 n'est pas ajouté à 65 et reste "m", sinon le chr() le passe en majuscule selon son code ASCII)
            if tourJoueur%2 == 0:
                self.plateau[1][x][y] = "M"                     #* remplace l'anneau par un marqueur en vue de la suite du tour
            else:
                self.plateau[1][x][y] = "m"
            return True, x, y
        else:
            return False, 0, 0 
        
    def checkCaseDeplacementAnneau(self, loopX, loopY):     #* vérifie si la case respecte les règles de déplacement de l'anneau
        coordsFinales = [0,0]
        stop = False
        if self.plateau[1][loopX][loopY] == "M" or self.plateau[1][loopX][loopY] == "m":
            self.marqueurSurChemin = True                   #* si la case est un marqueur, on indique que l'anneau passe sur des marqueurs
            coordsFinales[0], coordsFinales[1] = loopX,loopY
        elif self.plateau[1][loopX][loopY] == "A" or self.plateau[1][loopX][loopY] == "a":
            self.anneauSurChemin = True                     #* si la case est un anneau, on indique que l'anneau passe sur un anneau et ne peut donc pas continuer
            coordsFinales[0], coordsFinales[1] = loopX,loopY
        elif self.plateau[1][loopX][loopY] == 0:
            if self.marqueurSurChemin:                      #* si la case est vide et que l'anneau est passé par dessus des marqueurs, on le fait s'arrêter ici
                coordsFinales[0], coordsFinales[1] = loopX,loopY
                self.marqueurSurChemin = False
                stop = True
        return coordsFinales[0], coordsFinales[1], stop

        
    def checkLigneDeplacementAnneau(self, positionAnneauX, positionAnneauY):
        x,y = pygame.mouse.get_pos()
        x,y = x//50, y//25
        diffX = positionAnneauX-x
        diffY = positionAnneauY-y
        self.anneauSurChemin = False
        self.marqueurSurChemin = False
        coordsFinales = [0,0]
        if self.plateau[0][x][y] == 1:                     #* on vérifie que la case sélectionnée est une case jouable sur le plateau en lui même
            if self.plateau[1][x][y] == 0 or self.plateau[1][x][y] == "P":  #* vérifie que la case sélectionnée est vide
                if abs(diffX) == abs(diffY):                    #* on définit si la case sélectionnée est sur une diagonale ou sur une ligne horizontale/verticale
                    for i in range(1,abs(diffX)+1):             #* on répète jusqu'à la case sélectionnée
                        loopX = positionAnneauX-i*(diffX//abs(diffX))
                        loopY = positionAnneauY-i*(diffY//abs(diffY))
                        coordsFinales[0], coordsFinales[1], stop = self.checkCaseDeplacementAnneau(loopX, loopY)
                        if stop:
                            break
                    coordsFinales[0], coordsFinales[1] = loopX,loopY
                elif abs(diffX)%2 == 0 and abs(diffY) == 0 or abs(diffY)%2 == 0 and abs(diffX) == 0:
                    for i in range(1,(abs(diffX)+abs(diffY)+3)//2):
                        if abs(diffX) == 0:
                            loopX = positionAnneauX
                            loopY = positionAnneauY-i*(diffY//abs(diffY))*2
                            coordsFinales[0], coordsFinales[1], stop = self.checkCaseDeplacementAnneau(loopX, loopY)
                            if stop:
                                break
                        else:
                            loopX = positionAnneauX-i*(diffX//abs(diffX))*2
                            loopY = positionAnneauY
                            coordsFinales[0], coordsFinales[1], stop = self.checkCaseDeplacementAnneau(loopX, loopY)
                            if stop:
                                break
                    coordsFinales[0], coordsFinales[1] = loopX,loopY
        if coordsFinales[0] == x and coordsFinales[1] == y and self.anneauSurChemin == False:   #* si les coordonnées retenues par la méthode checkCaseDeplacementAnneau sont les mêmes que la case sélectionnée par l'utilisateur et qu'il n'y a pas d'anneau sur le chemin, alors on peut continuer
            return False
        else:
            return True
    
    def checkLigneDeplacementAnneauP2P(self, positionAnneauX, positionAnneauY,x,y):
        diffX = positionAnneauX-x
        diffY = positionAnneauY-y
        self.anneauSurChemin = False
        self.marqueurSurChemin = False
        coordsFinales = [0,0]
        if self.plateau[0][x][y] == 1:                     #* on vérifie que la case sélectionnée est une case jouable sur le plateau en lui même
            if self.plateau[1][x][y] == 0:                  #* vérifie que la case sélectionnée est vide
                if abs(diffX) == abs(diffY):                    #* on définit si la case sélectionnée est sur une diagonale ou sur une ligne horizontale/verticale
                    for i in range(1,abs(diffX)+1):             #* on répète jusqu'à la case sélectionnée
                        loopX = positionAnneauX-i*(diffX//abs(diffX))
                        loopY = positionAnneauY-i*(diffY//abs(diffY))
                        coordsFinales[0], coordsFinales[1], stop = self.checkCaseDeplacementAnneau(loopX, loopY)
                        if stop:
                            break
                    coordsFinales[0], coordsFinales[1] = loopX,loopY
                elif abs(diffX)%2 == 0 and abs(diffY) == 0 or abs(diffY)%2 == 0 and abs(diffX) == 0:
                    for i in range(1,(abs(diffX)+abs(diffY)+3)//2):
                        if abs(diffX) == 0:
                            loopX = positionAnneauX
                            loopY = positionAnneauY-i*(diffY//abs(diffY))*2
                            coordsFinales[0], coordsFinales[1], stop = self.checkCaseDeplacementAnneau(loopX, loopY)
                            if stop:
                                break
                        else:
                            loopX = positionAnneauX-i*(diffX//abs(diffX))*2
                            loopY = positionAnneauY
                            coordsFinales[0], coordsFinales[1], stop = self.checkCaseDeplacementAnneau(loopX, loopY)
                            if stop:
                                break
                    coordsFinales[0], coordsFinales[1] = loopX,loopY
        if coordsFinales[0] == x and coordsFinales[1] == y and self.anneauSurChemin == False:   #* si les coordonnées retenues par la méthode checkCaseDeplacementAnneau sont les mêmes que la case sélectionnée par l'utilisateur et qu'il n'y a pas d'anneau sur le chemin, alors on peut continuer
            return False
        else:
            return True
        
    def update_display(self,screen):
        self.affichagePlateau(screen)  #* affiche le plateau
        self.affichagePions(screen) #* affiche les pions si ils sont présent

    def del_possibles_moves(self):
        for i in range(len(self.plateau[1])):
            for u in range(len(self.plateau[1][i])):
                if self.plateau[1][i][u] == "P":
                    self.plateau [1][i][u] = 0

    def case_suivant_horizontale(self, i, x, y, direction):
        for u in range(2, 19, 2):
            print(i, x, y)
            if 0 <= x + i < self.taillePlateauY:
                if 0 <= x + i < len(self.plateau[0]) and 0 <= y < len(self.plateau[0][0]):
                    if self.plateau[0][x + i][y] == 1 and (self.plateau[1][x + i][y] == "m" or self.plateau[1][x + i][y] == "M"):

                        if direction == "right":
                            if 0 <= x + i + u < self.taillePlateauY:
                                if 0 <= x + i + u < len(self.plateau[1]) and 0 <= y < len(self.plateau[1][0]):
                                    if self.plateau[1][x + i + u][y] == 0:
                                        self.plateau[1][x + i + u][y] = "P"
                                    else:
                                        if 0 <= x + i + 2 < self.taillePlateauY:
                                            if 0 <= x + i + 2 < len(self.plateau[1]) and 0 <= y < len(self.plateau[1][0]):
                                                if self.plateau[1][x + i + 2][y] == "m" or self.plateau[1][x + i + 2][y] == "M":
                                                    if 0 <= x + i + u + 2 < self.taillePlateauY:
                                                        if 0 <= x + i + u + 2 < len(self.plateau[1]) and 0 <= y < len(self.plateau[1][0]):
                                                            if self.plateau[1][x + i + u + 2][y] == 0:
                                                                self.plateau[1][x + i + u + 2][y] = "P"
                                                            else:
                                                                break
                        elif direction == "left":
                            if 0 <= x - i - u >= 0:
                                if 0 <= x - i - u < len(self.plateau[1]) and 0 <= y < len(self.plateau[1][0]):
                                    if self.plateau[1][x - i - u][y] == 0:
                                        self.plateau[1][x - i - u][y] = "P"
                                    else:
                                        if 0 <= x - i - 2 >= 0:
                                            if 0 <= x - i - 2 < len(self.plateau[1]) and 0 <= y < len(self.plateau[1][0]):
                                                if self.plateau[1][x - i - 2][y] == "m" or self.plateau[1][x - i - 2][y] == "M":
                                                    if 0 <= x - i - u - 2 >= 0:
                                                        if 0 <= x - i - u - 2 < len(self.plateau[1]) and 0 <= y < len(self.plateau[1][0]):
                                                            if self.plateau[1][x - i - u - 2][y] == 0:
                                                                self.plateau[1][x - i - u - 2][y] = "P"
                                                            else:
                                                                break
            else:
                break
    def mouvements_possibles(self, x, y):
        #Vérifiez les mouvements horizontaux
        i = 2
        while True:
            if 0 <= x + i <= self.taillePlateauX:
                if len(self.plateau[0]) > x + i and len(self.plateau[1]) > x + i: #* check pour eviter out of range
                    self.case_suivant_horizontale(i,x,y,"right") #* check si la case suivant est un marqueur
                    if self.plateau[0][x + i][y] == 1 and self.plateau[1][x + i][y] == 0: #* on vérifie que la case est jouable et qu'elle est vide
                        self.plateau[1][x + i][y] = "P" #* on place un prévisu
                        #print("first",i)
                        # Nouvelle condition
                        if x + i + 2 < len(self.plateau[1]) and y < len(self.plateau[1][0]): 
                            if self.plateau[1][x + i + 2][y] == "m" or self.plateau[1][x + i + 2][y] == "M":
                                if 0 <= x + i + 4 <= self.taillePlateauX:
                                    if x + i + 4 < len(self.plateau[1]) and y < len(self.plateau[1][0]):
                                        if self.plateau[0][x + i + 4][y] == 1 and self.plateau[1][x + i + 4][y] == 0:
                                            self.plateau[1][x + i + 4][y] = "P"
                        i += 2
                    else:
                        break
                else:
                    break
        i = 2
        while True:
            if 0 <= x - i <= self.taillePlateauX:
                if len(self.plateau[0]) > x - i and len(self.plateau[1]) > x - i:
                    self.case_suivant_horizontale(i,x,y,"left")
                    if self.plateau[0][x - i][y] == 1 and self.plateau[1][x - i][y] == 0:
                        self.plateau[1][x - i][y] = "P"
                        #print("first",i)
                        # Nouvelle condition
                        if x - i - 2 < len(self.plateau[1]) and y < len(self.plateau[1][0]):
                            if self.plateau[1][x - i - 2][y] == "m" or self.plateau[1][x - i - 2][y] == "M":
                                if 0 <= x - i - 4 <= self.taillePlateauX:
                                    if x - i - 4 < len(self.plateau[1]) and y < len(self.plateau[1][0]):
                                        if self.plateau[0][x - i - 4][y] == 1 and self.plateau[1][x - i - 4][y] == 0:
                                            self.plateau[1][x - i - 4][y] = "P"
                        i += 2
                    else:
                        break
                else:
                    break
            else:
                break
        #
        ### Vérifiez les mouvements verticaux
        ##i = 2
        #while True:
        #    if 0 <= x - i < self.taillePlateauY:
        #        if len(self.plateau[0]) > y + i and len(self.plateau[1]) > y + i:
        #            if self.plateau[0][x][y + i] == 1 and self.plateau[1][x][y + i] == 0:
        #                self.plateau[1][x][y + i] = "P"
        #                #print("first",i)
        #                i += 2
        #            else:
        #                break
        #        else:
        #            break
        #i = 2
        #while True:
        #    if 0 <= x + i < self.taillePlateauX:
        #        if len(self.plateau[0]) > y - i and len(self.plateau[1]) > y - i:
        #            if self.plateau[0][x][y - i] == 1 and self.plateau[1][x][y - i] == 0:
        #                self.plateau[1][x][y - i] = "P"
        #                #print("first",i)
        #                i += 2
        #            else:
        #                break
        #        else:
        #            break
#
        # Vérifiez les mouvements diagonaux
        #for i in range(1, 10):
        #    if 0 <= x + i < self.taillePlateauX and 0 <= y + i < self.taillePlateauY:
        #        if self.plateau[0][x + i][y + i] == 1 and self.plateau[1][x + i][y + i] == 0:
        #            self.plateau[1][x + i][y + i] = "P"
        #        else:
        #            break
        #for i in range(1, 10):
        #    if 0 <= x - i < self.taillePlateauX and 0 <= y + i < self.taillePlateauY:
        #        if self.plateau[0][x - i][y + i] == 1 and self.plateau[1][x - i][y + i] == 0:
        #            self.plateau[1][x - i][y + i] = "P"
        #        else:
        #            break
        #for i in range(1, 10):
        #    if 0 <= x + i < self.taillePlateauX and 0 <= y - i < self.taillePlateauY:
        #        if self.plateau[0][x + i][y - i] == 1 and self.plateau[1][x + i][y - i] == 0:
        #            self.plateau[1][x + i][y - i] = "P"
        #        else:
        #            break
        #for i in range(1, 10):
        #    if 0 <= x - i < self.taillePlateauX and 0 <= y - i < self.taillePlateauY:
        #        if self.plateau[0][x - i][y - i] == 1 and self.plateau[1][x - i][y - i] == 0:
        #            self.plateau[1][x - i][y - i] = "P"
        #        else:
        #            break