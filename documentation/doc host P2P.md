#### fichier main.py 
#### fonction MainP2P

# MainP2P:

- on instancie une queue pour recevoir les données plateau et tour du client via le thread

- on écoute les tentative de connection sur l'ip local et sur le port

- durant que l'on écoute sur ces port on lance une interface via la def bind_and_accept

- une fois connecté on envoie et on recoit des messages pour tester la connection

- on démarre l'interface du jeu

- On charge les différents éléments de la page (titre, texte, boutons, etc...).

- On rentre dans la boucle principale du jeu:

- Si le joueur invité joue:

- On reçoit en constance les plateaux et tours envoyés depuis le serveur.

- On met à jour le plateau en fonction des informations reçues.

- Si le joueur hote joue:

- S'il n'a pas placé tous ses anneaux, il les place et envoie l'actualisation.

- Si tous les anneaux sont placés, on sélectionne un anneau à déplacer.

- Les prévisualisations s'affichent et on doit cliquer sur une case contenant une prévisualisation.

- Une fois l'anneau déplacé, si un alignement de marqueurs est détecté, on supprime l'alignement et l'anneau dernièrement déplacé.

- S'il n'y a pas d'alignement, on passe au prochain tour.