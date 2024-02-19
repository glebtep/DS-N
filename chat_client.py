import socket
import threading
from tkinter import *
from tkinter import simpledialog

class ChatClient:
    def __init__(self, master):
        self.master = master
        self.master.title("Chat Room")
        
        self.server_ip = simpledialog.askstring("Server IP", "Enter the server's IP:", parent=self.master)
        self.server_port = simpledialog.askinteger("Server Port", "Enter the server's port:", parent=self.master)
        self.username = simpledialog.askstring("Username", "Enter your username:", parent=self.master)
        
        self.text_area = Text(self.master, state='disabled')
        self.text_area.pack(padx=20, pady=10)
        
        self.msg_entry = Entry(self.master)
        self.msg_entry.pack(padx=20, pady=10)
        self.msg_entry.bind("<Return>", self.send_message)
        
        self.send_button = Button(self.master, text="Send", command=self.send_message)
        self.send_button.pack(pady=5)
        
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((self.server_ip, self.server_port))
        self.client_socket.send(self.username.encode('utf-8'))
        
        threading.Thread(target=self.receive_message, daemon=True).start()

    def send_message(self, event=None):
        message = self.msg_entry.get()
        self.client_socket.send(message.encode('utf-8'))
        self.msg_entry.delete(0, END)

    def receive_message(self):
        while True:
            try:
                message = self.client_socket.recv(1024).decode('utf-8')
                self.display_message(message)
            except Exception as e:
                print("Connection to server lost.")
                break

    def display_message(self, message):
        self.text_area.config(state='normal')
        self.text_area.insert(END, message + "\n")
        self.text_area.config(state='disabled')
        self.text_area.yview(END)

if __name__ == "__main__":
    root = Tk()
    app = ChatClient(root)
    root.mainloop()
