import pygame
from pion import *

class Plateau:
    def __init__(self, taillePlateau):
        self.taillePlateauY = taillePlateau+1
        self.taillePlateauX = int(taillePlateau*2)
        self.plateau = [list(),list()]
        self.pions = list()
        self.anneauxPlaces = 0
        self.marqueurSurChemin = False
        self.anneauSurChemin = False
    
    def get_taillePlateauY(self):
        return self.taillePlateauY
    
    def get_taillePlateauX(self):
        return self.taillePlateauX
    
    def get_plateau(self):
        return self.plateau
    
    def get_pions(self):
        return self.pions
    
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
        
    def pionsInitialisation(self):
        self.pions = [[0]*self.taillePlateauX for i in range(self.taillePlateauY)]


    def display(self):
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

    def displayPyGame(self):
        for i in range(self.taillePlateauY):
            for u in range(self.taillePlateauX):
                if self.plateau[0][i][u] == 1:
                    if self.plateau[1][i][u] == "a":
                        self.pions[i][u] = Pion(0, 0, 0, i*50, u*25, "a")
                    elif self.plateau[1][i][u] == "m":
                        self.pions[i][u] = Pion(0, 0, 0, i*50, u*25, "m")
                    elif self.plateau[1][i][u] == "A":
                        self.pions[i][u] = Pion(255, 255, 255, i*50, u*25, "A")
                    elif self.plateau[1][i][u] == "M":
                        self.pions[i][u] = Pion(255, 255, 255, i*50, u*25, "M")
                    else:
                        self.pions[i][u] = Pion(255, 255, 255, i*50, u*25, "x")
                if self.plateau[0][i][u] == 0:
                    self.pions[i][u] = Pion(0, 0, 0, i*50, u*25, "0")

    def affichagePlateau(self, screen):
        for i in range(len(self.plateau[0])):
            for u in range(len(self.plateau[0][i])):
                if self.plateau[0][i][u] == 1:
                    pygame.draw.rect(screen, (200,200,200), pygame.Rect((i*50, u*25, 50, 25)))
                if self.plateau[0][i][u] == 0:
                    pygame.draw.rect(screen, (50,50,50), pygame.Rect((i*50, u*25, 50, 25)))

    def affichagePions(self, screen):
        for i in range(len(self.pions)):
            for u in range(len(self.pions[i])):
                if self.pions[i][u].get_type() == "M" or self.pions[i][u].get_type() == "m":
                    pygame.draw.circle(screen, (self.pions[i][u].red,self.pions[i][u].green,self.pions[i][u].blue),(i*50+25,u*25+12), 8)
                elif self.pions[i][u].get_type() == "A" or self.pions[i][u].get_type() == "a":
                    pygame.draw.circle(screen, (self.pions[i][u].red,self.pions[i][u].green,self.pions[i][u].blue),(i*50+25,u*25+12), 12)
                    pygame.draw.circle(screen, (200,200,200),(i*50+25,u*25+12), 8)
                        
    def retournerMarqueurs(self, positionAnneauX, positionAnneauY):
        x,y = pygame.mouse.get_pos()
        x,y = x//50, y//25
        diffX = positionAnneauX-x
        diffY = positionAnneauY-y
        if abs(diffX) == abs(diffY):
            for i in range(1,abs(diffX)):
                loopX = positionAnneauX-i*(diffX//abs(diffX))
                loopY = positionAnneauY-i*(diffY//abs(diffY))
                if self.plateau[1][loopX][loopY] == "m":
                    self.plateau[1][loopX][loopY] = "M"
                elif self.plateau[1][loopX][loopY] == "M":
                    self.plateau[1][loopX][loopY] = "m"
        elif abs(diffX)%2 == 0 and abs(diffY) == 0 or abs(diffY)%2 == 0 and abs(diffX) == 0:
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

    def placementAnneaux(self, tourJoueur):
        x,y = pygame.mouse.get_pos()
        x,y = x//50, y//25
        if self.pions[x][y].get_type() == "x":
            if tourJoueur%2 == 0:
                self.plateau[1][x][y] = "A"
                tourJoueur+=1
                self.anneauxPlaces+=1
            else:
                self.plateau[1][x][y] = "a"
                tourJoueur+=1
                self.anneauxPlaces+=1
        return tourJoueur
 
    def selectionAnneaux(self, tourJoueur):
        x,y = pygame.mouse.get_pos()
        x,y = x//50, y//25
        if self.pions[x][y].get_type() == chr((tourJoueur%2)*32+65):
            if tourJoueur%2 == 0:
                self.plateau[1][x][y] = "M"
            else:
                self.plateau[1][x][y] = "m"
            return True, x, y
        else:
            return False, 0, 0    
        
    def checkCaseDeplacementAnneau(self, loopX, loopY):
        coordsFinales = [0,0]
        stop = False
        if self.plateau[1][loopX][loopY] == "M" or self.plateau[1][loopX][loopY] == "m":
            self.marqueurSurChemin = True
            coordsFinales[0], coordsFinales[1] = loopX,loopY
        elif self.plateau[1][loopX][loopY] == "A" or self.plateau[1][loopX][loopY] == "a":
            self.anneauSurChemin = True
            coordsFinales[0], coordsFinales[1] = loopX,loopY
        elif self.plateau[1][loopX][loopY] == 0:
            if self.marqueurSurChemin:
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
        if self.pions[x][y].get_type() == "x":
            if abs(diffX) == abs(diffY):
                for i in range(1,abs(diffX)+1):
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
        if coordsFinales[0] == x and coordsFinales[1] == y and self.anneauSurChemin == False:
            return False
        else:
            return True