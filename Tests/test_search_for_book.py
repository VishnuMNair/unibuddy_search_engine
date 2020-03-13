from unittest import TestCase

import requests

# import RESTServer.rest_server

test_url = 'http://localhost:5000/SearchBook'


class TestSearch_for_book(TestCase):
    def setUp(self):
        pass

    def test_search_for_book(self):
        query = ['is your problems', 'master of three']
        max_item = 3
        data = {'queries': query, 'K': max_item}
        response = requests.post(url=test_url, json=data)
        if response.status_code == 200:
            query_ret = []
            # r = response.json()
            for item in response.json():
                self.assertEqual(max_item, len(item))
                for val in item:
                    if val['query'] not in query_ret:
                        query_ret.append(val['query'])

            self.assertEqual(query, query_ret)

        else:
            self.fail(response.status_code)

    def tearDown(self):
        pass
