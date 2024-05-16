from tkinter import *
from plateau import *
import pygame
BG_COLOR = [50,50,50]
FONT_COLOR = [255,255,255]



def gestionClic(estClique):
    if pygame.mouse.get_pressed()[0]:
        if estClique == False:
            if pygame.mouse.get_pressed()[0]:
                return True
    else:
        return False

def renduTexteTourJoueur(tourJoueur):
    if tourJoueur%2 == 0:
        return "Au joueur Blanc de jouer"
    else:
        return "Au joueur Noir de jouer"

def debugCasePos():
    x,y = pygame.mouse.get_pos()
    x,y = x//50, y//25
    print(x,y)

def debugCaseValide(oldX,oldY):
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
    windowWidth = 600
    windowHeight = 600
    windowStayOpened = True
    screen = pygame.display.set_mode((windowWidth, windowHeight))
    screen.fill(BG_COLOR)


    objetPlateau = Plateau(10)
    objetPlateau.plateauInitialisation()

    estClique = False
    tourJoueur = 0
    anneauEnDeplacement = False
    positionAnneauX = 0
    positionAnneauY = 0

    while windowStayOpened:

        objetPlateau.affichagePlateau(screen)
        objetPlateau.affichagePions(screen)

        estClique = gestionClic(estClique)
        if estClique == True:
            if objetPlateau.get_anneauxPlaces() < 4:
                tourJoueur = objetPlateau.placementAnneaux(tourJoueur)
            else:
                #$debugCasePos()
                if anneauEnDeplacement:
                    anneauEnDeplacement = objetPlateau.checkLigneDeplacementAnneau(positionAnneauX, positionAnneauY)
                    if not anneauEnDeplacement:
                        tourJoueur = objetPlateau.placementAnneaux(tourJoueur)
                        objetPlateau.retournerMarqueurs(positionAnneauX, positionAnneauY)
                else:
                    anneauEnDeplacement, positionAnneauX, positionAnneauY = objetPlateau.selectionAnneaux(tourJoueur)

        #?fontColor = [255*((tourJoueur+1)%2),255*((tourJoueur+1)%2),255*((tourJoueur+1)%2)]
        tourJoueurTexte = renduTexteTourJoueur(tourJoueur)
        font = pygame.font.SysFont(None, 22)
        img = font.render(tourJoueurTexte, True, FONT_COLOR)
        screen.blit(img, (20, 20))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                windowStayOpened = False
        pygame.display.update()
    pygame.quit()

main()


#plateau = definitionPlateau(plateau, taillePlateauX-1, taillePlateauY-1)
#display(plateau, taillePlateauX, taillePlateauY)