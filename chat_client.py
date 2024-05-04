import socket
import threading
import os
from tkinter import filedialog
from gui import GUI  # Assuming you have a gui.py file

class ChatClient:
    def __init__(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect(('localhost', 5555))  # Update with your server IP and port

        # Initialize the GUI
        self.gui = GUI(self)
        self.gui.send_button.config(command=self.send_message)
        self.gui.send_file_button.config(command=self.send_file)

        # New code for receiving messages and files
        self.receive_thread = threading.Thread(target=self.receive_data)
        self.receive_thread.start()

    def send_message(self):
        message = self.gui.message_entry.get()
        self.display_message(f"You: {message}")
        self.client_socket.send(message.encode('utf-8'))

    def display_message(self, message):
        self.gui.chat_text.config(state="normal")
        self.gui.chat_text.insert("end", message + "\n")
        self.gui.chat_text.config(state="disabled")
        self.gui.message_entry.delete(0, "end")  # Clear the message entry

    def send_file(self):
        file_path = filedialog.askopenfilename()
        file_name = os.path.basename(file_path)

        # Send the file request to the server
        self.client_socket.send(f"FILE_REQUEST:{file_name}".encode('utf-8'))

        # Receive acknowledgment from the server
        ack = self.client_socket.recv(1024).decode('utf-8')

        if ack == "FILE_ACK":
            # Send the file content to the server
            with open(file_path, 'rb') as file:
                file_content = file.read()

            # Convert the entire message to bytes before sending
            message = f"FILE_CONTENT:{file_name}:{file_content.decode('utf-8')}".encode('utf-8')
            self.client_socket.send(message)

    def receive_data(self):
        while True:
            try:
                data = self.client_socket.recv(1024).decode('utf-8')
                if not data:
                    break

                # Check if the data is a file request or content
                if data.startswith("FILE_REQUEST"):
                    self.handle_file_request(data)
                elif data.startswith("FILE_CONTENT"):
                    self.handle_file_content(data)
                else:
                    self.display_message(data)

            except Exception as e:
                print(e)
                break

    def handle_file_request(self, data):
        # Extract the file name from the data
        file_name = data.split(":")[1]

        # Send acknowledgment to the server
        self.client_socket.send("FILE_ACK".encode('utf-8'))

        # Receive the file content from the server
        file_content = self.client_socket.recv(1024).decode('utf-8')

        # Save the file content to a file
        file_path = os.path.join("received_files", file_name)
        with open(file_path, 'ab') as file:  # Use binary mode
            file.write(file_content.encode('utf-8'))

        # Display a message in the chat about the received file
        self.display_message(f"File received: {file_name}")

    def handle_file_content(self, data):
        # Extract the file name and content from the data
        parts = data.split(":")
        file_name = parts[1]
        file_content = parts[2]

        # Save the file content to a file
        file_path = os.path.join("received_files", file_name)
        with open(file_path, 'ab') as file:  # Use binary mode
            file.write(file_content.encode('utf-8'))

    def run(self):
        self.gui.run()

if __name__ == "__main__":
    client = ChatClient()
    client.run()
