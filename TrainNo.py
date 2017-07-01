# -*- coding: utf-8 -*-
"""
Get the station which the train arrived
"""
import spider
import show
import requests
import json

class Station(object):
    def __init__(self, n, atime, stime, ltime):
        self.name = n
        self.arrive_time = atime
        self.stay_time = stime
        self.left_time = ltime

    def get_info(self):
        return [self.name, self.arrive_time, self.stay_time, self.left_time]



class TrainNo(object):
    def __init__(self, atrain, date):
        self.base_url = 'https://kyfw.12306.cn/otn/czxx/queryByTrainNo'
        self.train_no = atrain.get_train_no()
        self.start_city = spider.Tool.encode_city(atrain.get_start_city())
        self.dest_city = spider.Tool.encode_city(atrain.get_dest_city())
        self.date = date
        self.station_list = list()


    def build_url(self):
        params = list()
        params.append('train_no=%s' % (self.train_no))
        params.append('from_station_telecode=%s' % (self.start_city))
        params.append('to_station_telecode=%s' % (self.dest_city))
        params.append('depart_date=%s' % (self.date))
        return self.base_url + '?' + '&'.join(params)

    def send_requests(self):
        url = self.build_url()
        response = requests.get(url, verify=False)
        json_data = response.content
        data = json.loads(json_data)
        for item in data['data']['data']:
            station = Station(item['station_name'], item['arrive_time'],
                              item['stopover_time'], item['start_time'])
            self.station_list.append(station)
        return self.station_list

    def contruct_show_table(self):
        """for prettyshow"""
        res_list = list()
        res_list.append(['车站名', '到达时间', '停留时间', '出发时间'])
        for item in self.station_list:
            res_list.append(item.get_info())
        return json.dumps(res_list)

