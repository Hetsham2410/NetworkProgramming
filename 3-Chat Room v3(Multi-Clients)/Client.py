
import socket
import threading

host = '127.0.0.1'
port = 7002
alias = input("What is your alias: ")
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((host, port))



def receive_messages():
    global quite, alias
    while True:
        recv_data = client_socket.recv(1024).decode('utf-8')
        # print(message)

        if recv_data == "alias?":
            client_socket.send(alias.encode('utf-8'))
        elif recv_data == f'{alias}:{quite}':
            return
        else:
            print("")
            print(recv_data)


receive_thread = threading.Thread(target=receive_messages)
receive_thread.start()

while True:
    sent_data = f'{alias}:{input("")}'
    quite = "bye"
    if sent_data == f'{alias}:{quite}':
        client_socket.send(sent_data.encode("utf-8"))
        break
    client_socket.send(sent_data.encode('utf-8'))

client_socket.close()
