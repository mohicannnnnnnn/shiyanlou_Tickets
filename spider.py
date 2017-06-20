#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
author:endfighting
file:Get tickets msg from 12306 and provide some interface
"""
import re
import requests
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
from collections import OrderedDict
import json
import copy
import pdb
import urllib3
urllib3.disable_warnings()

class CityCode(object):
    def __init__(self, *city):
        """city code object"""
        ## bjb|北京北|VAP|beijingbei|bjb|0
        self.chinses_name = city[1]
        self.english_name = city[3]
        self.code = city[2]
        self.head_char = city[4]
        self.city_num = city[5]

    def get_city_code(self):
        return (self.chinses_name, self.code)

    def get_city_name(self):
        return (self.english_name, self.chinses_name)


class Tool(object):
    """provide some encode way"""
    FileName = 'city.log'
    CityCode = dict()
    EnCh = dict()
    # 在通过编号查询城市的时候需要用到
    CodeCity = None

    @classmethod
    def encode_city(cls, city_name):
        """from city name get city code"""
        return cls.CityCode[city_name]

    @classmethod
    def encode_date(cls, date):
        """get pro date format"""
        ## using re to check string as below way
        re_string = r'\d{4}[/\.-]\d{2}[/\.-]\d{2}'
        if not re.match(re_string, date):
            print 'date format error'
            return None
        new_format_date = date
        if date.count('.'):
            new_format_date = date.replace('.', '-')
        if date.count('/'):
            new_format_date = date.replace('/', '-')

        return new_format_date

    @classmethod
    def update_all_city(cls):
        """get all city code"""
        with open(cls.FileName, 'r') as fd:
            content = fd.read()
            # dislodge start str and the end str
            sp_content = content[:len(content)-2].split('@')
            for item in sp_content[1:]:
                city_item = item.split('|')
                ## for expand
                station = CityCode(*city_item)
                name = station.get_city_name()
                cls.EnCh[name[0]] = name[1]
                code = station.get_city_code()
                cls.CityCode[code[0]] = code[1]
            cls.CodeCity = {v:k for k,v in cls.CityCode.items()}

        #print 'length of dict is ', len(cls.EnCh)
        #for item in cls.CityCode:
        #    print item , cls.CityCode[item]
    @classmethod
    def from_code_get_city(cls, code):
        return cls.CodeCity[code]

#Tool.update_all_city()
#Tool.encode_city('北京')

class ATrain(object):
    def __init__(self):
        """"""
        self.train_no = None
        self.first_city = None
        self.start_city = None
        self.dest_city = None
        self.end_city = None
        self.start_time = None
        self.end_time = None
        self.need_time = None
        self.train_code = None
        #TZ, YZ, EZ, GRW, RW, YW, RZ, YZ, WZ
        #特等座, 一等座, 二等座, 高级软卧, 软卧, 硬卧,软座, 硬座, 无作
        #content is 有 无 数字
        self.left_num = None

        self.select_map = dict()

    def init_select_map(self):
        """when first call select function, it should init select map"""
        self.select_map['FirstCity'] = self.first_city
        self.select_map['StartCity'] = self.start_city
        self.select_map['EndCity'] = self.end_city
        self.select_map['DestCity'] = self.dest_city
        self.select_map['StartTime'] = self.start_time
        self.select_map['EndTime'] = self.end_time
        self.select_map['NeedTime'] = self.need_time
        self.select_map['TrainCode'] = self.train_code
        #TZ, YZ, EZ, GRW, RW, YW, RZ, YZ, WZ
        self.select_map['TDZ'] = self.left_num[0]
        self.select_map['YDZ'] = self.left_num[1]
        self.select_map['EDZ'] = self.left_num[2]
        self.select_map['GRW'] = self.left_num[3]
        self.select_map['RW'] = self.left_num[4]
        self.select_map['YW'] = self.left_num[5]
        self.select_map['RZ'] = self.left_num[6]
        self.select_map['YZ'] = self.left_num[7]
        self.select_map['WZ'] = self.left_num[8]

    def select(self, *chooice):
        """
        Here chooice we have :
            FirstCity
            StartCity
            EndCity
            DestCity
            StartTime
            EndTime
            NeedTime
            TrainCode
            TDZ, YDZ, EDZ, GRW, RW, YW, RZ, YZ, WZ
        """
        if not self.select_map:
            self.init_select_map()

        res_list = list()

        for item in chooice:
            res_list.append(self.select_map[item])

        return res_list


    def set_left_num(self, *count):
        """set the train left num"""
        self.left_num = copy.deepcopy(count)

    def set_city(self, fcity, ecity, scity, dcity):
        self.first_city = fcity
        self.end_city = ecity
        self.start_city = scity
        self.dest_city = dcity

    def set_train_code(self, code):
        self.train_code = code

    def set_train_time(self, stime, etime, ntime):
        self.start_time = stime
        self.end_time = etime
        self.need_time = ntime

    def set_train_no(self, no):
        """about train ways"""
        self.train_no = no

    def get_train_no(self):
        return self.train_no

    def get_start_city(self):
        return self.start_city

    def get_dest_city(self):
        return self.dest_city

    def get_train_code(self):
        return self.train_code


class OneItem(object):
    """once select record"""
    def __init__(self, start_date, start_city, dest_city, ticket_type='ADULT'):
        """provide citys and whther is a student ticket"""
        self.start_date = start_date
        self.start_city = start_city
        self.dest_city = dest_city
        self.ticket_type = ticket_type

    def set_type_as_student(self):
        """the type in 12306 student is 0x00"""
        self.ticket_type = '0X00'

    def set_type_as_adult(self):
        self.ticket_type = 'ADULT'

    def encode(self):
        """encode the arg as a list"""
        request_info = OrderedDict()
        request_info['leftTicketDTO.train_date'] = Tool.encode_date(self.start_date)
        request_info['leftTicketDTO.from_station'] = Tool.encode_city(self.start_city)
        request_info['leftTicketDTO.to_station'] = Tool.encode_city(self.dest_city)
        request_info['purpose_codes'] = self.ticket_type
        return request_info


class Spider(object):
    """define how to get 12306 interface"""
    URL = 'https://kyfw.12306.cn/otn/leftTicket/query'
    def __init__(self, scity, ecity, date):
        """one item need a spider to spider it"""
        self.item = OneItem(date, scity, ecity)
        self.json_data = None
        self.all_trains = list()
        self.select_head_map = {
            'FirstCity':'首发站',
            'EndCity':'终点站',
            'StartCity':'乘车车站',
            'DestCity':'目的车站',
            'StartTime':'发车时间',
            'EndTime':'预计到站时间',
            'NeedTime':'行车时间',
            'TrainCode':'列车号',
            'TDZ':'特等座',
            'YDZ':'一等座',
            'EDZ':'二等座',
            'GRW':'高级软卧',
            'RW':'软卧',
            'YW':'硬卧',
            'RZ':'软座',
            'YZ':'硬座',
            'WZ':'无座'
        }

    def select(self, *chooice):
        """select all trains"""
        res_list = list()
        head = [self.select_head_map[item] for item in chooice]
        #pdb.set_trace()
        res_list.append(head)
        for i in range(len(self.all_trains)):
            item = self.all_trains[i].select(*chooice)
            res_list.append(item)

        return json.dumps(res_list)

    def build_url(self):
        """build a url for send requests"""
        info_dict = self.item.encode()
        params = [key+'='+info_dict[key] for key in info_dict]
        return Spider.URL + '?' + '&'.join(params)

    def send_requests(self):
        """send requests and return json data"""
        #response = requests.get(Spider.URL, params=self.item.encode(),
        #                        verify=False)
        url = self.build_url()
        response = requests.get(url, verify=False)
        self.json_data = json.loads(response.content)

    def parse_json(self):
        for item in self.json_data['data']['result']:
            info = item.split('|')
            l1 = info[3:11]
            l2 = info[20:33]
            #特等座, 一等座, 二等座, 高级软卧, 软卧, 硬卧,软座, 硬座, 无作
            for index in range(len(l2)):
                if not l2[index]:
                    l2[index] = u'无'

            train = ATrain()
            ## left ticket num
            train.set_left_num(l2[12], l2[11], l2[10], l2[1], l2[3], l2[8],
                               l2[4], l2[9], l2[6])
            ## train code
            train.set_train_code(l1[0])
            ## citys
            citys = [Tool.from_code_get_city(item) for item in l1[1:5]]
            train.set_city(citys[0], citys[1], citys[2], citys[3])
            train.set_train_time(l1[5], l1[6], l1[7])
            train.set_train_no(info[2])
            self.all_trains.append(train)

    def get_one_train(self, traincode):
        for item in self.all_trains:
            if item.get_train_code() == traincode:
                return copy.deepcopy(item)

