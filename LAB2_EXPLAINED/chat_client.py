# Import necessary libraries
import socket  # For connecting to the server
import threading  # For handling incoming messages in a background thread
from tkinter import *  # For the GUI
from tkinter import simpledialog  # For prompt dialogs

# Class to encapsulate the client logic
class ChatClient:
    def __init__(self, master):
        self.master = master  # The main Tk window
        self.master.title("Chat Room")  # Window title
        
        # Prompt for server IP, port, and username
        self.server_ip = simpledialog.askstring("Server IP", "Enter the server's IP:", parent=self.master)
        self.server_port = simpledialog.askinteger("Server Port", "Enter the server's port:", parent=self.master)
        self.username = simpledialog.askstring("Username", "Enter your username:", parent=self.master)
        
        # Setup the main chat window
        self.text_area = Text(self.master, state='disabled')  # For displaying messages
        self.text_area.pack(padx=20, pady=10)
        self.msg_entry = Entry(self.master)  # For typing messages
        self.msg_entry.pack(padx=20, pady=10)
        self.msg_entry.bind("<Return>", self.send_message)  # Send message on Enter
        self.send_button = Button(self.master, text="Send", command=self.send_message)  # Send button
        self.send_button.pack(pady=5)
        
        # Connect to the server
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((self.server_ip, self.server_port))
        self.client_socket.send(self.username.encode('utf-8'))  # Send the username to the server
        
        # Start a thread to listen for messages from the server
        threading.Thread(target=self.receive_message, daemon=True).start()

    # Function to send messages
    def send_message(self, event=None):
        message = self.msg_entry.get()  # Get the message from the entry widget
        self.client_socket.send(message.encode('utf-8'))  # Send the message to the server
        self.msg_entry.delete(0, END)  # Clear the entry widget

    # Function to receive messages
    def receive_message(self):
        while True:
            try:
                message = self.client_socket.recv(1024).decode('utf-8')  # Receive a message
                self.display_message(message)  # Display it in the text area
            except Exception as e:
                print("Connection to server lost.")  # Error handling
                break

    # Function to display messages in the text area
    def display_message(self, message):
        self.text_area.config(state='normal')  # Enable text area to modify it
        self.text_area.insert(END, message + "\n")  # Insert the message
        self.text_area.config(state='disabled')  # Disable text area to prevent user editing
        self.text_area.yview(END)  # Scroll to the bottom

if __name__ == "__main__":
    root = Tk()  # Create the main window
    app = ChatClient(root)  # Instantiate the chat client
    root.mainloop()  # Start the Tk event loop
