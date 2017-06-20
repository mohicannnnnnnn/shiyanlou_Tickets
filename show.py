# -*- coding: utf-8 -*-
import spider
from prettytable import PrettyTable
import json


class prettyshow(object):
    """accept a json data, and use prettytable show"""
    def __init__(self, json_data):
        self.data = json.loads(json_data)

    def show(self):
        Table = PrettyTable(self.data[0])
        Table.padding_width = 1
        for i in range(1, len(self.data)):
            Table.add_row(self.data[i])
        print Table



def simple_show(spider):
    """show a spider"""
    x = PrettyTable(["列车号", "首发站", "终点站", "上车站", "下车站",
                     "上车时间", "到站时间", "乘车时间", "特等座",
                     "一等座", "二等座", "高级软卧", "软卧",
                     "硬卧", "软座", "硬座", "无座"])
    x.padding_width = 1 # One space between column edges and contents
    for item in spider.all_trains:
        item_list = list()
        item_list.append(item.train_code)
        item_list.append(item.first_city)
        item_list.append(item.end_city)
        item_list.append(item.start_city)
        item_list.append(item.dest_city)
        item_list.append(item.start_time)
        item_list.append(item.end_time)
        item_list.append(item.need_time)
        item_list.extend(item.left_num)
        x.add_row(item_list)
    print x

def constrcut_all_json(spider):
    """constrcuct a json consistent of all data"""
    head = ["列车号", "首发站", "终点站", "上车站", "下车站",
            "上车时间", "到站时间", "乘车时间", "特等座",
            "一等座", "二等座", "高级软卧", "软卧",
            "硬卧", "软座", "硬座", "无座"]

spider.Tool.update_all_city()
spider = spider.Spider('成都', '洛阳', '2017-07-01')
spider.send_requests()
spider.parse_json()
json_data = spider.select('TrainCode', 'StartCity', 'NeedTime', 'EDZ', 'YZ')
showobj = prettyshow(json_data)
showobj.show()
