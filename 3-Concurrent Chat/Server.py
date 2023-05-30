from socket import *
from threading import *

host = '127.0.0.1'
port = 7002

server_socket = socket(AF_INET, SOCK_STREAM)
server_socket.bind((host, port))
server_socket.listen()
print(f"Server listening on {host}:{port}")

clients = []
aliases = []


def broadcast_message(message, currentclient):
    for client in clients:
        try:
            if client != currentclient:
                client.send(message.encode('utf-8'))
        except:
            client.close()
            clients.remove(client)


def receive_messages(client):
    while True:
        try:
            message = client.recv(2048).decode('utf-8')
            broadcast_message(message, client)

        except KeyboardInterrupt:
            clients.remove(client)
            client.close()

while True:
    client_socket, client_address = server_socket.accept()
    clients.append(client_socket)
    print(f'connection is established with {str(client_address)}')
    client_socket.send("alias?".encode('utf-8'))
    alias = client_socket.recv(2048).decode('utf-8')
    aliases.append(alias)
    print(f'The alias of this client is {alias}')
    client_thread = Thread(target=receive_messages, args=(client_socket,))
    client_thread.start()

server_socket.close()
