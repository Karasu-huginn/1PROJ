#### MENUS

# Prérequis
- **import** : Importe les modules nécessaires au reste du code.
- **initialisation de Pygame** : Initialise les modules Pygame.

# Définition de la fenêtre
- **info_ecran** : Récupération des dimensions de l'écran.
- **fenetre** : Création de la fenêtre en mode plein écran.

# Chargement des ressources
- **chemin_police** : Chargement de la police depuis le dossier "fonts".
- **police** : Chargement de la police avec taille 46.
- **police_hover** : Chargement de la police avec taille 42 pour l'effet de survol.

- **chemin_image_titre** : Chemin vers l'image "yinsh.png".
- **image_titre** : Chargement de l'image du titre.
- **nouvelle_largeur_image, nouvelle_hauteur_image** : Redimensionnement de l'image du titre (65% de la taille originale).
- **image_titre_rect** : Gestion de la position de l'image sur la page (en haut à gauche).

- **chemin_image_fond** : Chemin vers l'image de fond "yinsh-plateau.jpeg".
- **image_fond** : Chargement de l'image de fond.
- **nouvelle_largeur_fond, nouvelle_hauteur_fond** : Redimensionnement de l'image de fond pour qu'elle couvre toute la fenêtre en gardant les proportions.
- **fond_transparent** : Création d'une surface temporaire avec effet de transparence à 50%.

# Affichage du texte
- **afficher_texte** : Fonction qui affiche du texte à une position donnée et renvoie le rectangle du texte pour détecter les clics.

# Menu principal
- **menu()** : 
  - Boucle principale pour gérer les événements et les interactions de l'utilisateur.
  - Gestion des événements de fermeture de la fenêtre et des touches clavier (ESC, 1, 2).
  - Remplissage de la fenêtre avec l'image de fond en transparence.
  - Affichage de l'image du titre.
  - Affichage des options de menu avec effet de survol.
  - Gestion des clics de souris pour les options "Jouer en ligne" et "Jouer sur ce PC".

# Gestion des options
- **jouer_en_ligne()** : Affiche un message pour lancer l'interface de jeu en ligne.
- **jouer_sur_ce_pc()** : 
  - Exécute le script `jouer_sur_ce_pc.py` avec `subprocess`.
  - Quitte Pygame et termine le programme en cas d'erreur.

# Exécution du menu
- **if __name__ == "__main__"** : Lance la fonction `menu()` pour démarrer le programme.

# Fonctiopn retour pour les autres menus

