**BG_COLOR**
**FONT_COLOR**
**BUTTON_BG_COLOR**
**BUTTON_BORDER_COLOR**
Sont l’équivalent de #define pour le préprocesseur, ce sont des variables globales constantes qu’on utilise comme alias afin de rendre le code plus lisible

*gestionClic* renvoie False si l’utilisateur ne clique pas, True lors de la première détection de clic et None lors de détections de clics successives après avoir déjà renvoyé True.

*renduTexteTourJoueur* renvoie le texte à afficher en fonction de si c’est le tour des Noirs ou le tour des Blancs.

*main* s’occupe du jeu en local. On commence par initialiser pygame, créer l’affichage et la variable qui permettra de garder la boucle de jeu ouverte. Ensuite on charge les différentes images à afficher dans l’interface et on leur applique les différentes paramètres de positionnement. Puis on instancie l’objet *objetPlateau* de la classe *Plateau* avec la taille désirée (par défaut 10) et on initialise le plateau complet. On initialise ensuite les différentes variables de gestion du jeu :
*estClique* (booléen) vérifie si l’utilisateur est en train de cliquer lors du passage de la boucle.
*tourJoueur* (int) décide qui doit jouer.
*anneauEnDeplacement* (booléen) permet de savoir si un anneau a été “transformé” en marqueur afin d’être déplacé.
*positionAnneauX* et Y (int) permettent d’enregistrer la position de l’anneau “transformé” en marqueur.
*pointsBlancs* et *pointsNoirs* (int) stockent les points des joueurs.
*marqueursAlignes* (booléen) permet de savoir si le joueur doit supprimer un anneau ou si il joue de manière classique.
*marqueursAlignesListe* (list) stocke les coordonnées par pairs des différents marqueurs alignés à supprimer du plateau.
*tourJoueurAlignement* (int) permet d’artificiellement “revenir en arrière” d’un tour lorsqu’un alignement se faire en fin de tour afin que le joueur puisse retirer son anneau et ses marqueurs malgré le passage de tour.
Ensuite on créée la zone de texte contenant les règles. On peut désormais rentrer dans la boucle principale de jeu qui s’exécutera tant que les joueurs peuvent continuer à jouer.
On commence par afficher les différents éléments de l’interface préparés plus tôt.
On vérifie si le joueur est en train de cliquer ou non, si les marqueurs ne sont pas alignés, que le joueur est en train de cliquer et qu’il y a des anneaux à placer, on place les anneaux par la méthode *placementAnneaux* et on incrémente *tourJoueur*, si il n’y a plus d’anneau à placer, on vérifie si on est déjà en train de déplacer un anneau ou pas, si c’est le cas on vérifie si l’anneau peut-être placé là où le joueur est en train de cliquer, si il peut alors *anneauEnDeplacement* est remit à False pour signifier que le déplacement est possible, donc on place l’anneau avec la même méthode qu’un placement d’anneau classique, on retourne les marqueurs avec la méthode *retournerMarqueurs*, on supprime les prévisualisations et on check les alignements et si il y en a on revient artificiellement un tour en arrière avec *tourJoueurAlignement* à -1 et stocke les pairs de coordonnées renvoyées par la méthode, si on est pas déjà en train de placer un anneau on récupère la position de la souris et on vérifie si la case cliqué est bien dans le plateau pour éviter un out of range, si c’est bon on vérifie si c’est bien un anneau, si c’est bon on génère les prévisualisations de mouvement, on vérifie ensuite qu’il y ait des marques sur le plateau, si c’est le cas on peut “transformer” l’anneau en marqueur.
Si la variable d’alignement des marqueurs est True et que le joueur est en train de cliquer,
on vérifie si la case sur laquelle le joueur clique est bien un anneau de sa couleur, puis on ajoute 1 au score, on supprime l’anneau avec la méthode *set_case_pion* et on supprime les marqueurs avec *suppressionMarqueursAlignement* en lui envoyant la liste des pairs de coordonnées des marqueurs à retirer. 
Ensuite on prépare différents textes à afficher à l’écran en fonction des différentes infos, les boutons d’intéraction et on affiche le tout à l’écran. Puis on gère les différents événements en fonction de si l’utilisateur clique sur la croix, appuie sur échap et autres.
Enfin une fois sortis de la boucle on affiche qui a gagné et on ferme pygame.

Pour *mainIA*, le fonctionnement est très similaire mais séparé en deux selon le tour du joueur et avec des méthodes générant des positions de cases aléatoires.