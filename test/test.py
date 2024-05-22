import socket

class Client:
    def __init__(self, host_name, port):
        self.host_name = host_name
        self.port = port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.buf_size = 1024

    def connect(self):
        self.client_socket.connect((self.host_name, self.port))
        print("Connected to server")

    def send_message(self, message):
        self.client_socket.send(message.encode())
        print(f"Sent message: {message}")

    def receive_message(self):
        message = self.client_socket.recv(self.buf_size).decode()
        print(f"Received message: {message}")
        return message

    def close(self):
        self.client_socket.close()
        print("Connection closed")

    def get_local_ip():
        host_name = socket.gethostname()
        local_ip = socket.gethostbyname(host_name)
        return local_ip
    def main ():
        if __name__ == "__main__":
            host_name = Client.get_local_ip()
            port = 1111
            client = Client(host_name, port)
            client.connect()


            message = ("Client : Bonjour le client est vivant ! :)")
            client.send_message(message)
            response = client.receive_message()
            client.close()


Client.main()