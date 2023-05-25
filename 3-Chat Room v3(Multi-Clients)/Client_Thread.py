
import socket
import threading

HOST = '127.0.0.1'
PORT = 7002
alias = input("Choose an alias >>> ")
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))



def receive_messages():
    while True:
        recv_data = client_socket.recv(1024).decode('utf-8')
        # print(message)
        if recv_data == "alias?":
            client_socket.send(alias.encode('utf-8'))
        else:
            print("")
            print(recv_data)


receive_thread = threading.Thread(target=receive_messages)
receive_thread.start()

while True:
    sent_data = f'{alias}: {input("")}'
    client_socket.send(sent_data.encode('utf-8'))

client_socket.close()
