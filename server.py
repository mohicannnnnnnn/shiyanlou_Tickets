#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
author:endfighting
file:Mainly provide some interface for client
"""
import socket
import json
import spider
#1. listen for client
#2. deal client push msg into mysql
#3. check 12306 in some time
class Server(object):
    def __init__ (self):
        spider.Tool.update_all_city()
        self.client_address = ('104.131.128.197', 8190)
        self.client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

        self.request_queue = dict()

    def listen(self):
        """
        many todos exception
        """
        self.client_socket.bind(self.client_address)
        self.client_socket.listen(5)
        while True:
            client, addr = self.client_socket.accept()
            print 'One clien connect<', addr, '>'
            ##deal pack
            buff = client.recv(100)
            i = buff.index('{')
            main_msg = buff[i:]
            all_length = int(buff[:i])

            lenth = len(main_msg)
            while True:
                if (lenth >= all_length):
                    break
                main_msg += client.recv(100)
                lenth += 100
            # save request
            self._push_request(client, main_msg)

            # get train info
            data = self._get_train_info(client)
            send_msg = str(len(data)) + data

            client.send(send_msg)
            client.close()
            print 'One client is over'

    def _push_request(self, client, data):
        """parse json requests"""
        req = json.loads(data)
        self.request_queue[client] = req

    def _get_train_info(self, client):
        req = self.request_queue[client]
        myspider = spider.Spider(req['start_station'].encode('utf8'),
                                req['dest_station'].encode('utf8'),
                                req['date'])
        ## pop from queu
        del self.request_queue[client]
        myspider.send_requests()
        myspider.parse_json()
        ##get dtrain or gtrain
        tmp = myspider.select('TrainCode', 'FirstCity', 'EndCity', 'StartTime',
                              'EndTime', 'TDZ', 'YDZ', 'EDZ', 'WZ')
        tmp = json.loads(tmp)
        gd_train = list()
        gd_train.append(tmp[0])
        for i in range(1, len(tmp)):
            if tmp[i][0].startswith('G') or tmp[i][0].startswith('D'):
                gd_train.append(tmp[i])

        ## get other train :k, z, t
        ttmp = myspider.select('TrainCode', 'FirstCity', 'EndCity', 'StartTime',
                              'EndTime', 'GRW', 'RW', 'YW', 'RZ', 'YZ', 'WZ')
        ttmp = json.loads(ttmp)
        other_train = list()
        other_train.append(ttmp[0])
        for i in range(1, len(ttmp)):
            if ttmp[i][0].startswith('T') or \
               ttmp[i][0].startswith('Z') or \
               ttmp[i][0].startswith('K'):
                other_train.append(ttmp[i])

        return json.dumps({'gdTrain':gd_train, 'otherTrain':other_train})

if __name__ == "__main__":
    server = Server()
    server.listen()
