# The chat server
import requests
import socket
import select
import sys
from _thread import *

# TODO these should be set in config files elsewhere
ip_addr = '127.0.0.1'
port = 4321
max_connections = 100
max_msg_size = 100

api_ip_addr = '127.0.0.1'
api_port = 5000


clients = []

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server.bind((ip_addr, port))
server.listen(max_connections)

def client_thread(conn, addr):
    conn.send('CONNECTION OPENED\n'.encode())
    while True:
        """
        Message format: '<token>\n<senderid>\n<roomid>\n<toptext>\n<bottomtext>\n<imgurl>'
        """
        message = conn.recv(max_msg_size)
        if message:
            mlines = message.splitlines()
            token = mlines[0] # TODO validate token
            sender_id = mlines[1]
            room = mlines[2]
            top = mlines[3]
            bottom = mlines[4]
            url = mlines[5]

            # send to API
            fields = {
                    'token': token,
                    'sender_id': sender_id,
                    'room_id': room,
                    'top': top,
                    'bottom': bottom,
                    'img_url': url
            }
            r = requests.post('http://' + api_ip_addr + ':' + str(api_port) + '/messages', data=fields)
            print(r.text)
            

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
