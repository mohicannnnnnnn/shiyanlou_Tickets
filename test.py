# -*- coding: utf-8 -*-
import spider
from prettytable import PrettyTable

spider.Tool.update_all_city()
spider = spider.Spider('成都', '洛阳', '2017-07-01')
spider.send_requests()
spider.parse_json()
spider.select('TrainCode', 'StartCity', 'NeedTime', 'EDZ')
