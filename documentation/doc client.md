#### fichier testcli.py 

# fonctions
- gestionClic : renvoie true uniquement si le clic de la souris est enfoncé alors qu'il ne l'était pas à la boucle précédente.

- renduTexteTourJoueur : renvoie le texte à afficher selon le tour du joueur.

- draw_button : fonction qui détermine la taille et la position des boutons.

# Yinsh client:

- On se connecte au serveur qui écoute sur son IP local (on saisit l'IP cible dans l'interface).

- On envoie des messages pour vérifier le fonctionnement du socket.

- On reçoit les messages du serveur pour le test.

- On instancie les classes Plateau et Client.

- On démarre un thread pour recevoir des messages contenant le plateau et le tour du joueur pour l'actualisation.

- On démarre l'interface du jeu client.

- On charge les différents éléments de la page (titre, texte, boutons, etc...).

- On rentre dans la boucle principale du jeu:

- Si le joueur hôte joue:

- On reçoit en constance les plateaux et tours envoyés depuis le serveur.

- On met à jour le plateau en fonction des informations reçues.

- Si le joueur invité joue:

- S'il n'a pas placé tous ses anneaux, il les place et envoie l'actualisation.

- Si tous les anneaux sont placés, on sélectionne un anneau à déplacer.

- Les prévisualisations s'affichent et on doit cliquer sur une case contenant une prévisualisation.

- Une fois l'anneau déplacé, si un alignement de marqueurs est détecté, on supprime l'alignement et l'anneau dernièrement déplacé.

- S'il n'y a pas d'alignement, on passe au prochain tour.

# Main :

- On déclare la variable ip étant une string vide.

- On récupère l'IP qui a été saisie dans l'interface.

- On lance le programme avec l'IP du serveur afin de s'y connecter.
