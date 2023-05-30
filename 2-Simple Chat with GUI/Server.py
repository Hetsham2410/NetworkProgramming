
import socket
import tkinter as tk
from tkinter import ttk
import threading


def send_message():
    message = input_entry.get()
    chat_listbox.insert(tk.END, f"Server: {message}")
    client_socket.send(message.encode())
    input_entry.delete(0, tk.END)


def receive_messages():
    while True:
        try:
            data = client_socket.recv(1024).decode()
            chat_listbox.insert(tk.END, f"Client: {data}")
        except:
            print("An error occurred while receiving messages.")
            client_socket.close()
            break


# Server configuration
host = '127.0.0.1'
port = 7002

# Create a socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((host, port))
server_socket.listen(1)
print("Server listening on {}:{}".format(host, port))

# Accept a client connection
client_socket, client_address = server_socket.accept()
print(f"Connected: {client_address}")

# Create GUI
window = tk.Tk()
window.title("Chat Server")
window.resizable(False, False)
s = ttk.Style()
# Create style used by default for all Frames
s.configure('TFrame', background="#005B5E")
s.configure("TButton",
            font=("algerian", 12),
            foreground="black",
            background="#A63012",
            relief="flat",
            borderwidth=0,
            width=10)

mainframe = ttk.Frame(window, style='TFrame')
mainframe.grid(column=0, row=0)
window.columnconfigure(0, weight=1)
window.rowconfigure(0, weight=1)

chat_listbox = tk.Listbox(mainframe, width=50, height=20, font=('algerian', 12))
chat_listbox.grid(column=1, row=1, padx=10, pady=10)

input_entry = ttk.Entry(mainframe, width=50)
input_entry.grid(column=1, row=2, padx=10, pady=10)

send_button = ttk.Button(mainframe, style="TButton", text="Send", command=send_message)
send_button.grid(column=1, row=3, padx=10, pady=10)

receive_thread = threading.Thread(target=receive_messages)
receive_thread.start()

window.mainloop()

# Close the socket when done
server_socket.close()
