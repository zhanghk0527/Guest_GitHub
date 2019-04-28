# -*- coding:utf-8 -*-

import requests
import json
import unittest

# 查询发布会接口
# url = "http://127.0.0.1:8000/api/get_event_list/"
# r = requests.get(url= url,params={'eid': 1})
# result = r.json()
# result_dump = json.dumps(result, indent=2, sort_keys=True, ensure_ascii=False)
# print (result_dump)
#
# assert result['status'] == 200
# assert result['message'] == 'success'
# assert result['data']['name'] == '小米5发布会'
# assert result['data']['limit'] == 2000
# assert result['data']['address'] == '北京市海淀区鸟巢'

class GetEventListTest(unittest.TestCase):

    def setUp(self):

        self.url = "http://127.0.0.1:8000/api/get_event_list/"

    def tearDown(self):
        pass

    def test_get_event_null(self):
        params = {'eid':''}
        r = requests.get(url=self.url, params=params)
        result = r.json()
        self.assertEqual(result['status'], 10021)
        self.assertEqual(result['message'], 'parameter error')

    def test_get_event_error(self):
        params = {'eid':'111000222'}
        r = requests.get(url=self.url, params= params)
        result = r.json()
        self.assertEqual(result['status'], 10022)
        self.assertEqual(result['message'], 'query result is empty')

    def test_get_event_success(self):
        params = {'eid':'1'}
        r = requests.get(url=self.url, params=params)
        result = r.json()
        self.assertEqual(result['status'], 200)
        self.assertEqual(result['message'], 'success')
        self.assertEqual(result['data']['name'], '小米5发布会')
        self.assertEqual(result['data']['address'], '北京市海淀区鸟巢')
        self.assertEqual(result['data']['start_time'], '2018-12-28T13:09:04')

if __name__ == '__main__':
    unittest.main()
