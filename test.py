# -*- coding: utf-8 -*-
import spider
from prettytable import PrettyTable

#spider.Tool.update_all_city()
#spider = spider.Spider('成都', '洛阳', '2017-07-01')
#spider.send_requests()
#spider.parse_json()
#spider.select('TrainCode', 'StartCity', 'NeedTime', 'EDZ')
def test(name, **key):
    print name
    for i in key:
        print i, key[i]
    print key['hgg']

test('hgg', hgg=100, lb=200)
