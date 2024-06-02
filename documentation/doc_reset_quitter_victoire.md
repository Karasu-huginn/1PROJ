#### PAGE DE FIN ET RESET

# Prérequis
- **import** : Importe les modules nécessaires (`pygame`, `sys`, `os`).
- **initialisation de Pygame** : Initialise les modules Pygame.

# Définition de la fenêtre
- **info_ecran** : Récupération des dimensions de l'écran.
- **fenetre** : Création de la fenêtre en mode plein écran.

# Chargement des ressources
- **chemin_police** : Chemin vers le fichier de police "RobotoSlab-Bold.ttf".
- **police_question** : Chargement de la police avec taille 60 pour la question.
- **police** : Chargement de la police avec taille 46.
- **police_hover** : Chargement de la police avec taille 54 pour l'effet de survol.

- **chemin_image_fond** : Chemin vers l'image de fond "yinsh-plateau.jpeg".
- **image_fond** : Chargement de l'image de fond.
- **nouvelle_largeur_fond, nouvelle_hauteur_fond** : Redimensionnement de l'image de fond pour qu'elle couvre toute la fenêtre en gardant les proportions.
- **fond_transparent** : Création d'une surface temporaire avec effet de transparence à 50%.

# Affichage du texte
- **afficher_texte** : Fonction qui affiche du texte à une position donnée et renvoie le rectangle du texte pour détecter les clics.

# Page de fin
- **page_de_fin()** : 
  - Boucle principale pour gérer les événements et les interactions de l'utilisateur.
  - Gestion des événements de fermeture de la fenêtre et de la touche ESC.
  - Remplissage de la fenêtre avec l'image de fond en transparence.
  - Affichage de la question centrée avec une plus grande taille de police.
  - Récupération des coordonnées de la souris.
  - Affichage des options de menu centrées et côte à côte avec effet de survol.
  - Gestion des clics de souris pour les options "Oui" et "Non".

# Exécution de la page de fin
- **if __name__ == "__main__"** : Lance la fonction `page_de_fin()` pour démarrer la page de confirmation de sortie.








#### PAGES DE VICTOIRE

# Prérequis
- **import** : Importe les modules nécessaires (`pygame`, `sys`).
- **initialisation de Pygame** : Initialise les modules Pygame.

# Définition de la fenêtre
- **screen_width, screen_height** : Définition des dimensions de la fenêtre (918x482).
- **screen** : Création de la fenêtre avec les dimensions définies.

# Chargement des ressources
- **background_image** : Chargement de l'image de fond "YINSH_board.png" avec `convert_alpha()` pour gérer la transparence.

# Création de la surface transparente
- **transparent_surface** : Création d'une surface avec transparence (170 sur 255).

# Ajout du texte
- **font** : Chargement de la police avec taille 74.
- **text** : Rendu du texte "Les blancs/noirs ont gagné" en noir.
- **text_rect** : Positionnement du texte au centre de l'écran.

# Ajout des boutons "quitter" et "recommencer"
- **render_text_with_hover** : Fonction pour rendre le texte avec un effet de survol (hover). Augmente la taille de la police si hover est vrai.
- **reset_font_size, quit_font_size** : Définition des tailles de police pour les boutons.
- **reset_text, reset_font** : Rendu du texte "recommencer" sans survol.
- **reset_text_rect** : Positionnement du texte "recommencer".
- **quit_text, quit_font** : Rendu du texte "quitter" sans survol.
- **quit_text_rect** : Positionnement du texte "quitter".

# Boucle principale
- **running** : Variable de contrôle pour la boucle principale.
- **mouse_pos** : Récupération de la position de la souris.

## Gestion des événements
- **pygame.QUIT** : Quitte la boucle principale si l'événement `QUIT` est détecté.
- **pygame.MOUSEBUTTONDOWN** : Vérifie si les boutons "quitter" ou "recommencer" sont cliqués.
  - **quit_text_rect.collidepoint** : Quitte le jeu si "quitter" est cliqué.
  - **reset_text_rect.collidepoint** : Ajoute la logique pour recommencer le jeu (à implémenter).

## Effet de survol
- **reset_hover** : Vérifie si la souris survole le texte "recommencer".
- **quit_hover** : Vérifie si la souris survole le texte "quitter".
- **render_text_with_hover** : Re-rendu des textes avec effet de survol si nécessaire.
- **reset_text_rect, quit_text_rect** : Mise à jour des rectangles après redimensionnement des textes.

## Affichage
- **screen.blit** : Affiche les éléments à l'écran dans l'ordre suivant :
  - Image de fond
  - Surface transparente
  - Texte central
  - Texte "recommencer"
  - Texte "quitter"

## Mise à jour de l'affichage
- **pygame.display.flip** : Met à jour l'affichage de la fenêtre.

# Fermeture de Pygame
- **pygame.quit()** : Ferme Pygame.
- **sys.exit()** : Quitte le programme.
