import os
import struct
from typing import BinaryIO

def send_file(file_path: str, sock: BinaryIO):
    file_name = os.path.basename(file_path)

    # Send the file request to the server
    sock.send(f"FILE_REQUEST:{file_name}".encode('utf-8'))

    # Receive acknowledgment from the server
    ack = sock.recv(1024).decode('utf-8')

    if ack == "FILE_ACK":
        # Send the file content to the server
        with open(file_path, 'rb') as file:
            file_content = file.read()

        # Convert the entire message to bytes before sending
        message = f"FILE_CONTENT:{file_name}:{file_content.decode('utf-8')}".encode('utf-8')
        sock.send(message)

def recv_file(sock: BinaryIO, save_path: str):
    # Extract the file name from the data
    file_name = sock.split(":")[1]

    # Send acknowledgment to the server
    sock.send("FILE_ACK".encode('utf-8'))

    # Receive the file content from the server
    file_content = sock.recv(1024).decode('utf-8')

    # Save the file content to a file
    file_path = os.path.join(save_path, file_name)
    with open(file_path, 'ab') as file:  # Use binary mode
        file.write(file_content.encode('utf-8'))
