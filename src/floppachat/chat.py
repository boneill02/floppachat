# The chat server
import socket
import select
import sys
from _thread import *

# TODO these should be set in config files elsewhere
ip_addr = '127.0.0.1'
port = 4321
max_connections = 100
max_msg_size = 100

clients = []

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server.bind((ip_addr, port))
server.listen(max_connections)

def client_thread(conn, addr):
    conn.send('CONNECTION OPENED\n'.encode())
    while True:
        """
        Message format: '<token>\n<roomid>\n<toptext>\n<bottomtext>\n<imgurl>'
        """
        message = conn.recv(max_msg_size)
        if message:
            mlines = message.splitlines()
            token = mlines[0] # TODO validate token
            room = mlines[1]
            top = mlines[2]
            bottom = mlines[3]
            url = mlines[4]
            print(message)

def broadcast(message, connection):
    for client in clients:
        if client != connection:
            try:
                client.send(message)
            except:
                client.close()
                remove(client)

def remove(connection):
    if connection in clients:
        clients.remove(connection)

while True:
    conn, addr = server.accept()
    clients.append(conn)
    print(addr[0] + ' connected\n')
    start_new_thread(client_thread, (conn, addr))

conn.close()
server.close()
