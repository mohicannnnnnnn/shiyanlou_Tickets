# -*- coding: utf-8 -*-
"""Mohican terminal command"""

import fire
import spider
import json
import show
import time

class Mohican(object):
    """get 12306 tickets infomation"""
    def __init__(self):
        spider.Tool.update_all_city()

    def _inner_requests(self, scity, ecity, date):
        self._myspider = spider.Spider(scity, ecity, date)
        self._myspider.send_requests()
        self._myspider.parse_json()

    def _deal_date(self, date):
        if not date:
            date = time.strftime('%Y-%m-%d',time.localtime(time.time()))
        return date


    def _judge_TrainCode(self, select_params):
        """judge whther TrainCode in params"""
        if 'TrainCode' in select_params:
            l = list(select_params)
            l.remove('TrainCode')
        else:
            l = select_params

        res_list = list()
        res_list.append('TrainCode')
        res_list.extend(select_params)
        return res_list

    def _get_train(self, key, scity, ecity, date, select_params):
        date = self._deal_date(date)
        select_params = self._judge_TrainCode(select_params)

        self._inner_requests(scity, ecity, date)
        json_data = self._myspider.select(*select_params)
        data = json.loads(json_data)

        new_res_list = list()
        new_res_list.append(data[0])
        for i in range(1, len(data)):
            if data[i][0].startswith(key):
                new_res_list.append(data[i])
            else:
                continue
        show_table = show.prettyshow(json.dumps(new_res_list))
        show_table.show()

    def GTrain(self, scity, ecity, date=None, *select_params):
        """Get the high-speed trains"""
        self._get_train('G', scity, ecity, date, select_params)


    def DTrain(self, scity, ecity, date=None, *select_params):
        """Get the motor trains"""
        self._get_train('D', scity, ecity, date, select_params)

    def GeneralTrain(self, scity, ecity, date=None, *select_params):
        """Get the general trains"""
        self._get_train('T', scity, ecity, date, select_params)
        self._get_train('K', scity, ecity, date, select_params)
        self._get_train('Z', scity, ecity, date, select_params)

    def Train(self, key, scity, ecity, date=None, *select_params):
        """Get the trains start with key"""
        self._get_train(key, scity, ecity, date, select_params)

    def AllTrain(self, scity, ecity, date=None, *select_params):
        """Get all trains"""
        date = self._deal_date(date)
        select_params = self._judge_TrainCode(select_params)

        self._inner_requests(scity, ecity, date)
        json_data = self._myspider.select(*select_params)

        show_table = show.prettyshow(json_data)
        show_table.show()

    def TimeSort(self, scity, ecity, date=None, *select_params):
        """Sort by need time"""
        date = self._deal_date(date)
        select_params = self._judge_TrainCode(select_params)

        self._inner_requests(scity, ecity, date)
        ## judge whther has NeedTime
        index = 1
        if 'NeedTime' in select_params:
            index = select_params.index('NeedTime')
        else:
            select_params.insert(1, 'NeedTime')

        json_data = self._myspider.select(*select_params)
        data = json.loads(json_data)

        new_list = data[1:]
        new_list.sort(key=lambda x:x[1])

        show_list = list()
        show_list.append(data[0])
        show_list.extend(new_list)
        show_table = show.prettyshow(json.dumps(show_list))
        show_table.show()




def main():
    fire.Fire(Mohican, name='Mohican')

if __name__ == '__main__':
    main()
