#Définition de la classe Plateau :

##Les attributs :
- *taillePlateauY* et *taillePlateauX* servent à définir la taille de la grille bidimensionnelle contenant soit les cases, soit les différents pions.
- *plateau* est une liste de listes contenant en indice 0 la liste bidimensionnelle représentant les cases jouables et en indice 1 les pions.
- *anneauxPlaces* représente le nombre d’anneaux placés par les joueurs au début de la partie afin de déterminer combien d’anneaux il reste à placer pour chaque joueur.

##Les méthodes :
On a d’abord 4 getters classiques, puis on a *get_pion* qui renvoie le pion d’une certaine case en lui passant en paramètre des coordonnées x et y.
Ensuite on a *get_case_pion* qui renvoie aussi le pion mais d’une case où la souris est positionnée.
Quant à *get_anneaux_nombre*, il renvoie le nombre exact d’anneaux blancs et noirs sur le plateau par deux variables différentes.

Pour les setters on en a que deux ; un premier qui permet de donner une certaine valeur de pion à la case où la souris où est positionnée et un second qui donne une certaine valeur de pion à une case selon des paramètres x et y

*plateauInitialisation* permet de créer un plateau grâce à la taille donnée en paramètre d’instanciation de *Plateau*, la hauteur étant deux fois plus élevée que la largeur.
Les deux premières lignes crééent un plateau remplis de 1 (qui représentent des cases jouables) dans la première sous-liste et de 0 dans la deuxième sous-liste. Ensuite on itère la liste des cases pour retirer toutes les cases non-jouables, donc on commence par retirer une case sur deux pour faire un quadrillage imitant des triangles afin d’avoir une simulation des intersections du plateau, puis on découpe les bords par différentes formules que je n’étaierai pas ici.

*affichagePions* permet d’afficher par l’interface graphique l’entièreté des pions stockés dans la deuxième sous-liste du plateau.

*retournerMarqueurs* permet d’inverser tous les marqueurs sur une ligne d’un point A à un point B, le dernier étant définit par des positions x et y selon la position de la souris à l’écran. On commence par vérifier si la ligne est une diagonale ou si c’est une ligne horizontale ou verticale. Puis on itère toutes les cases de la position d’origine à la position finale et on inverse le marqueur à chaque fois.

*retournerMarqueurIA* fait la même chose mais cette fois-ci la position finale est déterminée par x et y qui sont passés en paramètres.

*placementAnneaux* commence par récupérer la position de la souris pour en déterminer les coordonnées de la case où le joueur veut placer son anneau puis vérifie que cette case soit bien une case vide ou une case de prévisualisation, notée *P*. Si le placement est validé, *tourJoueur* est incrémenté et renvoyé au main.

*placementAnneauxIA* fait la même chose mais cette fois-ci la position finale est déterminée par x et y qui sont passés en paramètres.

*selectionAnneaux* récupère les coordonnées de la souris et vérifie que la case cliquée contient bien un anneau à déplacer de la couleur associée au tour du joueur puis le transforme en marqueur et renvoie un True à *anneauEnDeplacement* dans le main ainsi que les coordonnées de l’anneau à déplacer

*selectionAnneauxIA* fait la même chose mais cette fois-c i la position finale est déterminée par x et y qui sont passés en paramètres.

*checkDeplacementAnneau* vérifie si la case sélectionnée contient bien une prévisualisation, notée *P*. Renvoie True si validée.

*checkDeplacementAnneauIA* fait la même chose mais cette fois-ci la position finale est déterminée par x et y qui sont passés en paramètres.

*checkAlignementMarqueurs* itère l’entièreté du plateau, lorsqu’on tombe sur un marqueur on le stocke dans marque, puis on itère 4 cases dans chaque directions de la marque, à chaque itération, si on tombe sur un marqueur on ajoute les coordonnées de ce dernier sous forme d’une liste de deux entiers dans la liste *marqueursAlignesListe* et on incrémente alignement de 1, si alignement atteint 4 c’est qu’il y a bien un alignement de 5 marqueurs donc on renvoie True ainsi que la liste des coordonnées de marqueurs
*suppressionMarqueursAlignement* itère une liste des pairs de coordonnées et met à 0 tous les pions aux coordonnées données.