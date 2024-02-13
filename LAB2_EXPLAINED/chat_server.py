# Import necessary libraries
import socket  # For network connections
import threading  # To handle multiple clients simultaneously

# Global set to track connected clients
clients = set()

# Global dictionary to map clients to their usernames
usernames = {}

# Function to broadcast messages to all connected clients
def broadcast_message(message):
    for client in clients:  # Iterate over all clients
        client.send(message.encode('utf-8'))  # Send the message, encoded to bytes

# Function to handle communication with a client
def handle_client(client_socket):
    while True:  # Keep listening for messages from the client
        try:
            message = client_socket.recv(1024).decode('utf-8')  # Receive message
            if message == 'quit':  # Check if the message is a quit command
                break  # Exit the loop to disconnect the client
            broadcast_message(f"{usernames[client_socket]} says: {message}")  # Broadcast the received message
        except:
            break  # In case of error, exit the loop and disconnect
    client_socket.close()  # Close the client socket
    clients.remove(client_socket)  # Remove the client from the global set
    broadcast_message(f"{usernames[client_socket]} has left the chat.")  # Notify others of the disconnection

# Function to start the server and accept connections
def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Create a socket object
    server_socket.bind(('127.0.0.1', 12345))  # Bind the socket to an address and port
    server_socket.listen()  # Start listening for incoming connections
    
    while True:  # Infinite loop to accept all incoming connections
        client_socket, _ = server_socket.accept()  # Accept a connection
        clients.add(client_socket)  # Add the client to the global set
        thread = threading.Thread(target=handle_client, args=(client_socket,))  # Create a thread for the client
        thread.start()  # Start the client thread

if __name__ == "__main__":
    start_server()  # Call the function to start the server
