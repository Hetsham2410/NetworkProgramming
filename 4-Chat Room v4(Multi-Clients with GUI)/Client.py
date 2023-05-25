import socket
import tkinter as tk
from tkinter import ttk
import threading

def send_message():
    message = input_entry.get()
    chat_listbox.insert(tk.END, f"{alias}: {message}")
    server_socket.send(message.encode())
    input_entry.delete(0, tk.END)

def receive_messages():
    while True:
        try:
            data = server_socket.recv(1024).decode()
            chat_listbox.insert(tk.END, data)
        except:
            print("An error occurred while receiving messages.")
            server_socket.close()
            break

# Server configuration
host = '127.0.0.1'
port = 7002

# Create a socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.connect((host, port))
print("Connected to the server.")

# Get client alias
alias = input("Enter your alias: ")
server_socket.send(alias.encode())

# Create GUI
window = tk.Tk()
window.title(f"{alias}")

mainframe = ttk.Frame(window, padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky=(tk.N, tk.W, tk.E, tk.S))
window.columnconfigure(0, weight=1)
window.rowconfigure(0, weight=1)

chat_listbox = tk.Listbox(mainframe, width=50, height=20)
chat_listbox.grid(column=1, row=1, padx=10, pady=10, sticky=(tk.W, tk.E))

input_entry = ttk.Entry(mainframe, width=50)
input_entry.grid(column=1, row=2, padx=10, pady=10, sticky=(tk.W, tk.E))

send_button = ttk.Button(mainframe, text="Send", command=send_message)
send_button.grid(column=1, row=3, padx=10, pady=10, sticky=(tk.W, tk.E))

for child in mainframe.winfo_children():
    child.grid_configure(padx=5, pady=5)

receive_thread = threading.Thread(target=receive_messages)
receive_thread.start()

window.mainloop()

# Close the socket when done
server_socket.close()
