#!/usr/bin/env python3
import socket
import select
import sys

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

if len(sys.argv) != 3:
    print("Correct usage: <prog> host port")
    exit()

ip = str(sys.argv[1])
port = int(sys.argv[2])
server.connect((ip, port))

while True:
    sockets_list = [sys.stdin, server]
    read_sockets,write_socket, error_socket = select.select(sockets_list,[],[])
    for socks in read_sockets:
        if socks == server:
            message = socks.recv(2048)
            print(message)
        else:
            message = input('token: ')
            message += input('sender id: ')
            message += input('room id: ')
            message += input('top text: ')
            message += input('bottom text: ')
            message += input('img url: ')
            '<token>\n<senderid>\n<roomid>\n<toptext>\n<bottomtext>\n<imgurl>'
            server.send(message.encode())
            sys.stdout.write('<YOU> ' + message)
            sys.stdout.flush()

server.close()
