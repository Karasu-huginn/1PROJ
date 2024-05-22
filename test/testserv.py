import socket

class Server:
    def __init__(self, host_name, port):
        self.host_name = host_name
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.buf_size = 1024

    def bind(self):
        self.server_socket.bind((self.host_name, self.port))
        self.server_socket.listen()
        print(f"Server listening on {self.host_name}:{self.port}")

    def accept_connection(self):
        connection, addr = self.server_socket.accept()
        print(f"Connected to {addr}")
        return connection, addr

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

    def main ():
        if __name__ == "__main__":
            host_name = Server.get_local_ip()
            port = 1111
            server = Server(host_name, port)
            server.bind()


            connection, addr = server.accept_connection()
            message = server.receive_message(connection)
            response = ("Server : Bonjour le serveur est aussi vivant ! :D")
            server.send_message(connection, response)
            server.close(connection)



Server.main()