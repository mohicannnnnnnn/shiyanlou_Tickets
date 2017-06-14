#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
author:endfighting
file:Get tickets msg from 12306 and provide some interface
"""
import re

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

    @classmethod
    def encode_city(cls, city_name):
        """from city name get city code"""
        return cls.CityCode[city_name]

    @classmethod
    def encode_date(cls, date):
        """get pro date format"""
        ## using re to check string as below way
        re_string = r'\d{4}[/\.-]\d{2}[/\.-]\d{2}'
        if re.match(re_string, date):
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

        #print 'length of dict is ', len(cls.EnCh)
        #for item in cls.CityCode:
        #    print item , cls.CityCode[item]

Tool.update_all_city()
Tool.encode_city('北京')

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
        request_info  = {
            'leftTicketDTO.train_date': Tool.encode_date(self.start_date),
            'leftTicketDTO.from_station': Tool.encode_city(self.start_city),
            'leftTicketDTO.to_station': Tool.encode_city(self.dest_city),
            'purpose_codes':self.ticket_type
        }
        return request_info




class Spider(object):
    pass

#Tool.update_all_city()
