import socket
from plateau import *
from queue import Queue
import pygame
import threading
BUFF_SIZE = 2048

class Server:
    def __init__(self, host_name, port):
        self.host_name = host_name
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.buf_size = 2048
        self.connected = False
        self.stop_event = threading.Event()

    def accept_connection(self):
        connection, addr = self.server_socket.accept()
        print(f"Connected to client : {addr}")
        self.connected = True

    def bind_and_accept(self, ip):
        self.server_socket.bind((self.host_name, self.port))
        self.server_socket.listen()

        print(f"Server listening on {self.host_name}:{self.port}")
        pygame.init()
        info = pygame.display.Info()
        WIDTH, HEIGHT = info.current_w, info.current_h
        screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
        pygame.display.set_caption("Loading Page")
        font = pygame.font.Font(None, 74)
        button_font = pygame.font.Font(None, 40)

        #* Texte "En attente du client..."
        text_surface = font.render(f"En attente du client sur {ip}...", True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2))

        #* Position et dimensions du bouton "Revenir au menu"
        menu_button_rect = pygame.Rect(WIDTH - 300, HEIGHT - 100, 250, 60)

        #* Variables pour l'animation des points
        dots_animation_timer = pygame.time.get_ticks()
        dots_animation_delay = 500
        dots_count = 0

        clock = pygame.time.Clock()

        thread = threading.Thread(target=self.accept_connection)
        thread.start()

        while not self.connected:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    self.close()
                    return None, None, False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    #* Si le user clique sur le bouton "Revenir au menu"
                    if menu_button_rect.collidepoint(event.pos):
                        self.close()
                        return None, None, False

            #* Animation des points
            current_time = pygame.time.get_ticks()
            if current_time - dots_animation_timer >= dots_animation_delay:
                dots_animation_timer = current_time
                dots_count = (dots_count + 1) % 4

            screen.fill((128, 128, 128))
            #* Affichage du texte "En attente du client..." avec les trois petits points animés
            text_with_dots = "En attente du client sur " + ip + "." * dots_count
            text_surface = font.render(text_with_dots, True, (0, 0, 0))
            text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            screen.blit(text_surface, text_rect)
            #* Affichage du bouton "Revenir au menu"
            pygame.draw.rect(screen, (50, 50, 50), menu_button_rect, border_radius=10)
            pygame.draw.rect(screen, (255, 255, 255), menu_button_rect, 2, border_radius=10)
            menu_text = button_font.render("Revenir au menu", True, (255, 255, 255))
            menu_text_rect = menu_text.get_rect(center=menu_button_rect.center)
            screen.blit(menu_text, menu_text_rect)
            pygame.display.flip()
            clock.tick(30)

            #* Acceptation de la connexion
            connection, addr = self.server_socket.accept()
            print(f"Connected to client : {addr}")
            self.connected = True

        return connection, addr, self.connected
        
    def interfaceP2Phost(self, ip):
        #* Définition de la fenêtre en plein écran
        
        info = pygame.display.Info()
        WIDTH, HEIGHT = info.current_w, info.current_h
        screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
        pygame.display.set_caption("Loading Page")

        #* Définition de la police de caractère
        font = pygame.font.Font(None, 74)
        button_font = pygame.font.Font(None, 40)

        #* Texte "En attente du client..."
        text_surface = font.render(f"En attente du client sur {ip}...", True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2))

        #* Position et dimensions du bouton "Revenir au menu"
        menu_button_rect = pygame.Rect(WIDTH - 300, HEIGHT - 100, 250, 60)

        #* Variables pour l'animation des points
        dots_animation_timer = pygame.time.get_ticks()
        dots_animation_delay = 500
        dots_count = 0

        clock = pygame.time.Clock()


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.stop_event.set()
                break
            if event.type == pygame.MOUSEBUTTONDOWN:
                #* Si le user clique sur le bouton "Revenir au menu"
                if menu_button_rect.collidepoint(event.pos):
                    self.stop_event.set()
                    break
        dots_animation_timer, dots_count = self.animate_dots(dots_animation_timer, dots_animation_delay, dots_count)
        screen.fill((128, 128, 128))
        #* Affichage du texte "En attente du client..." avec les trois petits points animés
        text_with_dots = "En attente du client sur " + ip + "." * dots_count
        text_surface = font.render(text_with_dots, True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(text_surface, text_rect)
        #* Affichage du bouton "Revenir au menu"
        pygame.draw.rect(screen, (50, 50, 50), menu_button_rect, border_radius=10)
        pygame.draw.rect(screen, (255, 255, 255), menu_button_rect, 2, border_radius=10)
        menu_text = button_font.render("Revenir au menu", True, (255, 255, 255))
        menu_text_rect = menu_text.get_rect(center=menu_button_rect.center)
        screen.blit(menu_text, menu_text_rect)
        pygame.display.flip()
        clock.tick(30)
        
    def animate_dots(self, dots_animation_timer, dots_animation_delay, dots_count):
        current_time = pygame.time.get_ticks()
        if current_time - dots_animation_timer > dots_animation_delay:
            dots_count = (dots_count + 1) % 4  #* 0, 1, 2, 3, 0, 1, 2, 3,...
            dots_animation_timer = current_time
        return dots_animation_timer, dots_count

    def receive_message(self, connection):
        message = connection.recv(self.buf_size).decode()
        print(f"Received message: {message}")
        return message

    def send_message(self, connection, message):
        connection.send(message.encode())
        print(f"Sent message: {message}")

    def close(self, connection):
        connection.close()
        print("Connection closed")

    def get_local_ip():
        host_name = socket.gethostname()
        local_ip = socket.gethostbyname(host_name)
        return local_ip
            

    def receive_messages_thread(self, queue,connection): #* ajoute le plateau et le tourjoueur à la queue (utilise dans le thread)
        while self.connected:
            message_recu = self.receive_message(connection)
            if message_recu.startswith("plateau:"):
                queue.put(str(message_recu))
                print("un plateau à été ajouté à la queue")
            elif message_recu.startswith("tour:"):
                queue.put(str(message_recu))
                print("un tour à été ajouté à la queue")