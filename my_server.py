import socket
import threading

serversock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

serversock.bind(("127.0.0.1", 5555))  # Binds the socket to our ip and the port

serversock.listen(1)

clients_list = []
names_list = []


def broadcast(message,client_sock):

    global clients_list
    global names_list

    for client in clients_list:
        if client != client_sock:

            client.send(message)

def handle_client(client):

    global clients_list
    global names_list

    # Save the client to the clients pool
    clients_list.append(client)
    # Now telling client to choose nickname
    client.send("NICK".encode("utf-8"))

    # Expects to recieve a nick from client
    nick = client.recv(1024).decode('utf-8')
    names_list.append(nick)
    client.send("SUCCESS".encode('utf-8'))
    broadcast(f"{nick} has join the chatroom".encode('utf-8'), client)

    while True:
        try:
            message = client.recv(1024)
            nick_index = clients_list.index(client)
            broadcast((f"{names_list[nick_index]}: ").encode('utf-8') + message, client)
        except ConnectionResetError:
            nick_index = clients_list.index(client)
            client.close()
            clients_list.remove(client)
            broadcast(f"User {names_list[nick_index]} has left the chatroom".encode('utf-8'), client)
            names_list.pop(nick_index)
            break

def handshake(client_sock):
    # Save the client to the clients pool
    clients_list.append(client_sock)
    # Now telling client to choose nickname
    client_sock.send("NICK".encode("utf-8"))

    # Expects to recieve a nick from client
    nick = client_sock.recv(1024).decode('utf-8')
    names_list.append(nick)
    client_sock.send("SUCCESS".encode('utf-8'))
    broadcast(f"{nick} has join the chatroom".encode('utf-8'),client_sock)
def connect():

    global clients_list
    global names_list
    while True:
        client_sock, client_addr = serversock.accept()
        # threading.Thread(target=handshake,args=(client_sock,)).start()
        threading.Thread(target=handle_client, args=(client_sock,)).start()


connect()