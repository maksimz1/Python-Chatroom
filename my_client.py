import socket
import threading

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_ip = "127.0.0.1"
server_port = 5555
def handshake():
    client_socket.connect((server_ip,server_port))
    # At this point, server should tell us to enter a nickname
    response1 = client_socket.recv(1024).decode('utf-8')
    while(True):
        if response1 == "NICK":
            my_nick = input("Please choose nickname: ")
            client_socket.send(my_nick.encode('utf-8'))
            break
    while(True):
        response2 = client_socket.recv(1024).decode('utf-8')
        if response2 == "SUCCESS":
            print(f"CONNECTION SUCCESSFUL, Welcome to chat {my_nick}")
            break

def recieve():
    global client_socket
    while True:
        try:
            message = client_socket.recv(1024)
            print(message.decode('utf-8'))
        except:
            client_socket.close()
            break
def send_message():
    global client_socket
    while True:
        message = input()
        try:
            client_socket.send(message.encode('utf-8'))
        except:
            client_socket.close()
            break

handshake()

recieve_thread = threading.Thread(target=recieve)
send_thread = threading.Thread(target=send_message)
recieve_thread.start()
send_thread.start()
