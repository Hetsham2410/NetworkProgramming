from socket import *
from threading import *

host = '127.0.0.1'
port = 7002

s = socket(AF_INET, SOCK_STREAM)
s.bind((host, port))
s.listen()
print(f"Server listening on {host}:{port}")

clients = []
aliases = []


def sendMessageToAllUser(message, currentclient):
    for client in clients:
        try:
            if client != currentclient:
                client.send(message.encode('utf-8'))
        except:
            client.close()
            clients.remove(client)


def connectNewUser(client):
    while True:
        try:
            message = client.recv(2048).decode('utf-8')
            sendMessageToAllUser(message, client)

        except KeyboardInterrupt:
            clients.remove(client)
            client.close()

while True:
    client, add = s.accept()
    clients.append(client)
    print(f'connection is established with {str(add)}')
    client.send("alias?".encode('utf-8'))
    alias = client.recv(2048).decode('utf-8')
    aliases.append(alias)
    print(f'The alias of this client is {alias}')
    client_thread = Thread(target=connectNewUser, args=(client,))
    client_thread.start()
s.close()
