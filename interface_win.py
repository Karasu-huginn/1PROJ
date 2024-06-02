import pygame
import sys

def render_text_with_hover(text, font_size, color, hover):
    if hover:
        font = pygame.font.Font(None, font_size + 5)  # Augmentation de taille réduite
    else:
        font = pygame.font.Font(None, font_size)
    return font.render(text, True, color), font



def win(message):
    # Initialisation de Pygame
    pygame.init()

    # Définir les dimensions de la fenêtre
    screen_width = 918
    screen_height = 482
    screen = pygame.display.set_mode((screen_width, screen_height))

    # Charger l'image de fond
    background_image = pygame.image.load("YINSH_board.png").convert_alpha()

    # Créer une surface transparente
    transparent_surface = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
    transparent_surface.fill((255, 255, 255, 170))  # Remplir avec une couleur blanche avec transparence

    # Ajouter du texte
    font = pygame.font.Font(None, 74)
    text = font.render(message, True, (0, 0, 0))
    text_rect = text.get_rect(center=(screen_width // 2, screen_height // 2))

    # Ajouter les boutons "quitter" et "recommencer"


    reset_font_size = 36
    quit_font_size = 36

    quit_text, quit_font = render_text_with_hover("quitter", quit_font_size, (0, 0, 0), False)
    quit_text_rect = quit_text.get_rect(center=(screen_width - 45, screen_height - 40))  # Recentrer le texte

    # Boucle principale
    running = True
    while running:
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if quit_text_rect.collidepoint(event.pos):
                    running = False
                    pygame.quit()
                    return 1


        # Vérifier si la souris est au-dessus des textes
        quit_hover = quit_text_rect.collidepoint(mouse_pos)

        # Re-rendre les textes avec l'effet de hover si nécessaire
        quit_text, quit_font = render_text_with_hover("quitter", quit_font_size, (0, 0, 0), quit_hover)

        # Mettre à jour les rectangles après avoir redimensionné les textes
        quit_text_rect = quit_text.get_rect(center=(screen_width - 65, screen_height - 40))  # Recentrer le texte

        # Afficher l'image de fond
        screen.blit(background_image, (0, 0))

        # Ajouter la surface transparente par-dessus l'image
        screen.blit(transparent_surface, (0, 0))

        # Afficher le texte central
        screen.blit(text, text_rect)

        # Afficher les texte "quitter" et "recommencer"
        screen.blit(quit_text, quit_text_rect)

        # Mettre à jour l'affichage
        pygame.display.flip()

    pygame.quit()
    sys.exit()
