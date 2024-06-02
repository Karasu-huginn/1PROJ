import pygame
import sys
import os
#import subprocess


BLANC = (180, 180, 180)
NOIR = (0, 0, 0)

def afficher_texte(fenetre,texte, x, y, couleur, font):
    texte_surface = font.render(texte, True, couleur)
    texte_rect = texte_surface.get_rect(topleft=(x, y))
    fenetre.blit(texte_surface, texte_rect)
    return texte_rect
def menu():
    pygame.init()
    info_ecran = pygame.display.Info()
    largeur_fenetre = info_ecran.current_w
    hauteur_fenetre = info_ecran.current_h

    fenetre = pygame.display.set_mode((largeur_fenetre, hauteur_fenetre), pygame.FULLSCREEN)

    # Chemin vers le fichier de police
    chemin_police = os.path.join('fonts', 'RobotoSlab-Bold.ttf')  # Utilisez le répertoire et le nom corrects de votre fichier

    # Utilisation de la nouvelle police
    police = pygame.font.Font(chemin_police, 46)
    police_hover = pygame.font.Font(chemin_police, 42)

    # Chemin vers l'image du titre
    chemin_image_titre = os.path.join('yinsh.png')

    # Charger l'image du titre
    image_titre = pygame.image.load(chemin_image_titre)

    # Redimensionner l'image du titre (par exemple, augmenter de 20%)
    largeur_image, hauteur_image = image_titre.get_size()
    nouvelle_largeur_image = int(largeur_image * 0.65)
    nouvelle_hauteur_image = int(hauteur_image * 0.65)
    image_titre = pygame.transform.scale(image_titre, (nouvelle_largeur_image, nouvelle_hauteur_image))

    # Obtenir le rectangle de l'image redimensionnée
    image_titre_rect = image_titre.get_rect(topleft=(80, 50))

    # Chemin vers l'image de fond
    chemin_image_fond = os.path.join('yinsh-plateau.jpeg')

    # Charger l'image de fond
    image_fond = pygame.image.load(chemin_image_fond)

    # Redimensionner l'image de fond pour qu'elle couvre toute la fenêtre en gardant les proportions
    ratio = max(largeur_fenetre / image_fond.get_width(), hauteur_fenetre / image_fond.get_height())
    nouvelle_largeur_fond = int(image_fond.get_width() * ratio)
    nouvelle_hauteur_fond = int(image_fond.get_height() * ratio)
    image_fond = pygame.transform.scale(image_fond, (nouvelle_largeur_fond, nouvelle_hauteur_fond))

    # Surface temporaire pour l'effet de transparence
    fond_transparent = pygame.Surface((nouvelle_largeur_fond, nouvelle_hauteur_fond))
    fond_transparent.blit(image_fond, (0, 0))
    fond_transparent.set_alpha(128)  # 50% de transparence




    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_1:
                    pygame.quit()
                    return 1
                elif event.key == pygame.K_2:
                    pygame.quit()
                    return 2

        fenetre.fill(BLANC)
        
        # Afficher l'image de fond avec transparence
        fenetre.blit(fond_transparent, ((largeur_fenetre - nouvelle_largeur_fond) // 2, (hauteur_fenetre - nouvelle_hauteur_fond) // 2))
        
        # Affichage de l'image du titre en haut à gauche
        fenetre.blit(image_titre, image_titre_rect)
        
        # Récupérer les coordonnées de la souris
        mouse_x, mouse_y = pygame.mouse.get_pos()

        # Afficher les options de menu avec effet de survol
        rect_jouer_en_ligne = afficher_texte(fenetre,"1. Jouer en ligne", 50, hauteur_fenetre // 2.5 + 50, NOIR, police_hover if 50 < mouse_x < 50 + police_hover.size("1. Jouer en ligne")[0] and hauteur_fenetre // 2.5 + 50 < mouse_y < hauteur_fenetre // 2.5 + 50 + police_hover.size("1. Jouer en ligne")[1] else police)
        rect_jouer_sur_ce_pc = afficher_texte(fenetre,"2. Jouer sur ce PC", 50, hauteur_fenetre // 2.5 + 100 + 30, NOIR, police_hover if 50 < mouse_x < 50 + police_hover.size("2. Jouer sur ce PC")[0] and hauteur_fenetre // 2.5 + 100 + 30 < mouse_y < hauteur_fenetre // 2.5 + 100 + 30 + police_hover.size("2. Jouer sur ce PC")[1] else police)
        
        # Récupérer les boutons cliqués de la souris
        mouse_click = pygame.mouse.get_pressed()
        
        # Vérifier si le bouton "Jouer en ligne" est cliqué
        if rect_jouer_en_ligne.collidepoint((mouse_x, mouse_y)) and mouse_click[0] == 1:
            pygame.quit()
            return 1
        
        # Vérifier si le bouton "Jouer sur ce PC" est cliqué
        if rect_jouer_sur_ce_pc.collidepoint((mouse_x, mouse_y)) and mouse_click[0] == 1:
            pygame.quit()
            return 2
            
        pygame.display.flip()

#def jouer_en_ligne():
#    print("Lancement de l'interface Jouer en ligne")
#
#def jouer_sur_ce_pc():
#    try:
#        chemin_script = os.path.join('jouer_sur_ce_pc.py')
#        subprocess.run(['python', chemin_script])
#        pygame.quit()
#        sys.exit()
#    except Exception as e:
#        print(f"Erreur lors de l'exécution de {chemin_script} : {e}")
#        pygame.quit()
#        sys.exit()
#
#if __name__ == "__main__":