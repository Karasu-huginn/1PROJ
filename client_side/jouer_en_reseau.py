import pygame
import sys
from menu import *

# Initialisation de Pygame
pygame.init()

# Définition des couleurs
BLANC = (255, 255, 255)
NOIR = (0, 0, 0)

# Obtenir les dimensions de l'écran
info_ecran = pygame.display.Info()
largeur_fenetre = info_ecran.current_w
hauteur_fenetre = info_ecran.current_h

# Paramètres de la fenêtre
fenetre = pygame.display.set_mode((largeur_fenetre, hauteur_fenetre), pygame.FULLSCREEN)
pygame.display.set_caption("Menu Yinch - Jouer sur ce PC")

# Police de texte
police = pygame.font.Font(None, 36)

def afficher_texte(texte, x, y, couleur):
    texte_surface = police.render(texte, True, couleur)
    texte_rect = texte_surface.get_rect(center=(x, y))
    fenetre.blit(texte_surface, texte_rect)
    return texte_rect  # Retourne le rectangle englobant le texte

def jouer_sur_ce_pc():
    while True:
        fenetre.fill(BLANC)
        afficher_texte("Jouer sur ce PC", largeur_fenetre // 2, hauteur_fenetre // 6, NOIR)
        afficher_texte("1. Jouer contre une IA", largeur_fenetre // 2, hauteur_fenetre // 3, NOIR)
        afficher_texte("2. Jouer à deux", largeur_fenetre // 2, hauteur_fenetre // 2.5, NOIR)
        retour_menu_rect = afficher_texte("Appuyez sur Echap pour revenir au menu", largeur_fenetre // 2, hauteur_fenetre - 100, NOIR)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return  # Retour au menu
                elif event.key == pygame.K_1:
                    jouer_contre_ia()
                elif event.key == pygame.K_2:
                    jouer_a_deux()

            # Récupérer les coordonnées du clic de la souris
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Clic gauche
                    if retour_menu_rect.collidepoint(event.pos):  # Vérifie si les coordonnées du clic sont à l'intérieur du rectangle du texte
                        menu()

        pygame.display.flip()

def jouer_contre_ia():
    # Mettez ici le code de l'interface "Jouer contre une IA"
    print("Lancement de l'interface Jouer contre une IA")

def jouer_a_deux():
    # Mettez ici le code de l'interface "Jouer à deux"
    print("Lancement de l'interface Jouer à deux")

if __name__ == "__main__":
    jouer_sur_ce_pc()
