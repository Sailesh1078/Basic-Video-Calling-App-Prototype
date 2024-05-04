import socket
import os
import threading

class FileTransferServer:
    def __init__(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind(('localhost', 5556))  # Use a different port for file transfer
        self.server_socket.listen()

        self.clients = []

    def start(self):
        print("File Transfer Server is listening for connections...")
        while True:
            client_socket, client_address = self.server_socket.accept()
            print(f"File Transfer Connection from {client_address}")
            self.clients.append(client_socket)

            # Start a new thread to handle the client
            client_handler = threading.Thread(target=self.handle_client, args=(client_socket,))
            client_handler.start()

    def handle_client(self, client_socket):
        try:
            file_name = client_socket.recv(1024).decode('utf-8')
            print(f"Receiving file: {file_name}")

            # Specify the path to save the received file
            file_path = os.path.join("received_files", file_name)

            # Receive the file content
            with open(file_path, 'wb') as file:
                while True:
                    data = client_socket.recv(1024)
                    if not data:
                        break
                    file.write(data)

            print(f"File received: {file_name}")
        except Exception as e:
            print(f"Error handling file transfer: {e}")
        finally:
            client_socket.close()

if __name__ == "__main__":
    file_transfer_server = FileTransferServer()
    file_transfer_server.start()
