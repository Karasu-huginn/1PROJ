#### Classe Client/ serveur
# Attributs de classe
-hostname : Adresse IP de connexion

-port : Port utilisé par le socket

-client_socket : Socket utilisé pour la connexion TCP

-buff_size : Taille du buffer

-connected : Statut de la connexion (vrai si connecté, faux sinon)


# Méthodes
-connect : Effectue la connexion avec la cible.

-send_message : Envoie des messages via le socket.

-receive_message : Reçoit des messages via le socket.

-close : Ferme la connexion entre le client et le serveur.

-get_local_ip : Récupère l’adresse IP locale de l’hôte.

-receive_message_thread : Reçoit en continu des mises à jour, comme celles d’un plateau de jeu et du tour en cours.


###################################################


