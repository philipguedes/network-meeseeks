import os
import requests
from functools import wraps


NEUBOT_ADDR = os.getenv('NEUBOT_ADDR', 'http://127.0.0.1:9774')


def make_request(path):
    def wrapper(func):    
        @wraps(func)
        def func_wrapper(self, *args, **kwargs):
            url = '{}/api{}'.format(NEUBOT_ADDR, path)
            res = requests.get(url)
            data = res.json()
            return func(self, *args, data=data, **kwargs)
        return func_wrapper
    return wrapper


class NeubotService(object):
    def __init__(self):
        endpoints = self.__get_endpoits()

    @make_request('/')
    def __get_endpoits(self, **kwargs):
        return kwargs.get('data')

    @make_request('/config')
    def get_config(self, **kwargs):
        return kwargs.get('data')

    def get_dash_lag(self, elapsed, target, iteration):
        # TODO: Implement data
        return None

    @make_request('/data?test=dash')
    def dash_data(self, **kwargs):
        data = kwargs.get('data')
        dataset = {}
        for elem in data:
            ts = elem['whole_test_timestamp']
            if ts not in dataset:
                dataset[ts] = {
                    'freeze':[],
                    'iteration': 0,
                    'total_elapsed': 0,
                    'total_elapsed_target': 0
                }
            total_elapsed = dataset[ts]['total_elapsed'] + elem['elapsed']
            total_elapsed_target = dataset[ts]['total_elapsed_target'] + elem['elapsed_target']
            
            dataset[ts]['total_elapsed'] = total_elapsed
            dataset[ts]['total_elapsed_target'] = total_elapsed_target 
            
            dataset[ts]['iteration'] += 1
            lag_data = self.get_dash_lag(total_elapsed, total_elapsed_target, elem['iteration'])

            if lag_data is not None:
                dataset[ts]['freeze'].append(lag_data)

        return dataset

    @make_request('/data?test=speedtest')
    def speedtest_data(self, **kwargs):
        data = kwargs.get('data')
        dataset = {}
        for elem in data:
            ts = elem['timestamp']
            dataset[ts] = {
                'goodput': elem['download_speed'],
                'upload': elem['upload_speed'],
                'latency': elem['latency'],
                'rtt': elem['connect_time']
            }
        return dataset
        
    @make_request('/data?test=raw')
    def raw_data(self):
        pass


    @make_request('/data?test=bittorrent')
    def bittorrent_data(self):
        pass
