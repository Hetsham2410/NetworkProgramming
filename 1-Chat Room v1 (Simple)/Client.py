from socket import *

host = "127.0.0.1"
port = 7002

client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect((host, port))
print("Connected to the server.")

while True:
    sent_data = input("Client:")
    if sent_data.lower() == 'bye':
        client_socket.send(sent_data.encode("utf-8"))
        break
    client_socket.send(sent_data.encode("utf-8"))

    recv_data = client_socket.recv(2048).decode("utf-8")
    if recv_data.lower() == 'bye':
        break
    print("Server:", recv_data)

client_socket.close()
