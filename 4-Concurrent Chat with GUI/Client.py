import socket
import tkinter as tk
from tkinter import ttk
import threading

host = '127.0.0.1'
port = 7002

# Create a socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.connect((host, port))
print("Connected to the server.")

# Get client alias
alias = input("Enter your alias: ")
server_socket.send(alias.encode())


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


# Create GUI
window = tk.Tk()
window.title(f"{alias} Chat")

window.resizable(False, False)

style = ttk.Style()
# Create style used by default for all Frames
style.configure('TFrame',
                background="#A74F4F")
style.configure("TButton",
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
