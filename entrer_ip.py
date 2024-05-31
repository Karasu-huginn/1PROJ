import pygame
import pygame.locals as pl
import sys

def interface():
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    GRAY = (128, 128, 128)
    LIGHT_GRAY = (200, 200, 200)
    DARK_GRAY = (50, 50, 50)
    pygame.init()

    # Définition de la fenêtre en plein écran
    info = pygame.display.Info()
    windowWidth = 600       #* Largeur fenêtre (int)
    windowHeight = 410      #* Hauteur fenêtre (int)
    screen = pygame.display.set_mode((windowWidth, windowHeight))
    pygame.display.set_caption("Input IP Address")

    # Définition de la police de caractère
    font = pygame.font.Font(None, 50)
    input_font = pygame.font.Font(None, 50)
    button_font = pygame.font.Font(None, 40)

    # Texte au-dessus de l'input
    text_surface = font.render("Veuillez rentrer une adresse IP", True, BLACK)
    text_rect = text_surface.get_rect(center=(windowWidth // 2, windowHeight // 3))
    


    # Position et dimensions de l'input box
    input_rect = pygame.Rect(windowWidth // 2 - 200, windowHeight // 2, 400, 50)
    color_inactive = LIGHT_GRAY
    color_active = WHITE
    

    color = color_inactive
    active = False
    text_input = ''
    # Bouton "Envoyer"
    send_button_rect = pygame.Rect(input_rect.right + 10, input_rect.y, 50, 50)

    # Bouton "Quitter"
    quit_button_rect = pygame.Rect(windowWidth - 220, windowHeight - 100, 200, 60)

    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Activation/désactivation de l'input
                if input_rect.collidepoint(event.pos):
                    active = not active
                else:
                    active = False
                color = color_active if active else color_inactive
                # Bouton "Envoyer"
                if send_button_rect.collidepoint(event.pos):
                    print("Adresse IP envoyée:", text_input)
                    pygame.quit()
                    return text_input  # Retourne la valeur de text_input
                # Bouton "Quitter"
                if quit_button_rect.collidepoint(event.pos):
                    running = False
            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        print("Adresse IP entrée:", text_input)
                        text_input = ''
                    elif event.key == pygame.K_BACKSPACE:
                        text_input = text_input[:-1]
                    else:
                        text_input += event.unicode

        screen.fill(GRAY)
        screen.blit(text_surface, text_rect)

        # Affichage de l'input box
        pygame.draw.rect(screen, color, input_rect, border_radius=10)
        txt_surface = input_font.render(text_input, True, BLACK)
        screen.blit(txt_surface, (input_rect.x + 5, input_rect.y + 5))


        # Affichage du bouton "Envoyer"
        pygame.draw.rect(screen, DARK_GRAY, send_button_rect, border_radius=10)
        pygame.draw.polygon(screen, WHITE, [(send_button_rect.centerx, send_button_rect.y + 15),
                                            (send_button_rect.centerx - 10, send_button_rect.y + 35),
                                            (send_button_rect.centerx + 10, send_button_rect.y + 35)])
        

        # Affichage du bouton "Quitter"
        pygame.draw.rect(screen, DARK_GRAY, quit_button_rect, border_radius=10)
        quit_text = button_font.render("Quitter", True, WHITE)
        quit_text_rect = quit_text.get_rect(center=quit_button_rect.center)
        screen.blit(quit_text, quit_text_rect)

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()
    sys.exit()  # Ferme le programme si le bouton "Quitter" est cliqué
