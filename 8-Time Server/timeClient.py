import socket

# create a TCP/IP socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = '127.0.0.1'
port = 7003
# connect the socket to the server's address and port

client_socket.connect((host, port))

recv_message = client_socket.recv(1024)
current_time = recv_message.decode('utf-8')
print('Current Time: ', current_time)
client_socket.close()
