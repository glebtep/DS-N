import socket
import threading

clients = set()
usernames = {}

def broadcast_message(message):
    for client in clients:
        client.send(message.encode('utf-8'))

def handle_client(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if message:
                broadcast_message(f"{usernames[client_socket]} says: {message}")
            if message.lower() == "quit":
                raise Exception("User quit")
        except:
            print(f"{usernames[client_socket]} disconnected")
            clients.remove(client_socket)
            broadcast_message(f"{usernames[client_socket]} has left the chat.")
            client_socket.close()
            break

def receive_connections(server_socket):
    while True:
        client_socket, _ = server_socket.accept()
        client_socket.send("Username?".encode('utf-8'))
        username = client_socket.recv(1024).decode('utf-8')
        usernames[client_socket] = username
        clients.add(client_socket)
        print(f"{username} joined the chat")
        broadcast_message(f"{username} has joined the chat")
        thread = threading.Thread(target=handle_client, args=(client_socket,))
        thread.start()

if __name__ == "__main__":
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('127.0.0.1', 12345))
    server_socket.listen()
    print("Server listening for connections...")
    receive_connections(server_socket)
