
from socket import *
import datetime

host = "127.0.0.1"
port = 7003
server_socket = socket(AF_INET, SOCK_STREAM)

server_socket.bind((host, port))
server_socket.listen(1)
print("Time Server listening on {}:{}".format(host, port))
while True:
    client_socket, client_address = server_socket.accept()
    print("Connection to: ", client_address[1])
    current_time = str(datetime.datetime.now())
    client_socket.sendall(current_time.encode())
# close the connection
client_socket.close()