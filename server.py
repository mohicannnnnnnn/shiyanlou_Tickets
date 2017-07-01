#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
author:endfighting
file:Mainly provide some interface for client
"""
import socket
#1. listen for client
#2. deal client push msg into mysql
#3. check 12306 in some time
class Server(object):
    def __init__ (self):
        self.client_address = ('127.0.0.1', 8190)
        self.client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

    def listen(self):
        self.client_socket.bind(self.client_address)
        self.client_socket.listen(5)
        client, addr = self.client_socket.accept()
        print client, addr

    def send_json(self):
        pass


if __name__ == "__main__":
    server = Server()
    server.listen()
