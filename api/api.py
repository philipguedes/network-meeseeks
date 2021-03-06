# coding: utf-8

from __future__ import print_function
import sys
import zerorpc
import json
import tempfile
from src.utils import get_logger
from src.adapters.voip import VoipAdapter
from src.machines.dash import DashStateMachine
from src.machines.voip import VoipStateMachine
from src.machines.gaming import GamingStateMachine
from src.machines.lstreaming import LStreamingStateMachine


LOGGER = get_logger(__name__)


class NetworkUserApi(object):
    """
    Translate the network tests result in a way
    more user-friendly.
    """
    def __init__(self):
        self.graph_creator = None
        self.__initialize_machines()
        self.__initialize_adapters()

    def __initialize_machines(self):
        self.voip_machine = VoipStateMachine()
        self.dash_machine = DashStateMachine()
        self.gaming_machine = GamingStateMachine()
        self.lstreaming_machine = LStreamingStateMachine()

    def __initialize_adapters(self):
        self.voip_adapter = self.voip_machine.adapter
        self.dash_adapter = self.dash_machine.adapter
        self.gaming_adapter = self.gaming_machine.adapter
        self.lstreaming_adapter = self.lstreaming_machine.adapter
        
    def dash(self):
        """
        Translate parameters related to Dynamic Adaptive Streaming 
        over HTTP (DASH).
        It uses Netflix and Youtube as an example

        It considers mostly the bandwidth (for video quality) | download speed.
        """
        self.dash_adapter.update_data()
        return self.dash_adapter.data

    def lstreaming(self):
        """
        Translate parameters related to HTTP Live Streaming (HLS)
        It uses Twitch and Youtube as an example

        It considers mostly the packet loss and the upload speed.
        """
        self.lstreaming_adapter.update_data()
        return self.lstreaming_adapter.data

    def gaming(self):
        """
        Translate parameters related to Gamming.
        It uses League of Legends and Dota2 as an example

        It considers mostly the packet loss.
        It should consider either the human reaction time.
        """
        self.gaming_adapter.update_data()
        return self.gaming_adapter.data

    def voip(self):
        """
        Translate parameters related to Voip services.
        It uses Skype, Discord and Hangouts as an example.

        If using only audio, it should consider the packet loss.
        If using video too, it should consider the bandwidth also.
        """
        self.voip_adapter.update_data()
        return self.voip_adapter.data

    def get_images(self):
        data = dict(
            voip=self.voip(),
            gaming=self.gaming(),
            lstreaming=self.lstreaming(),
            dash=self.dash()
        )
        for _, elem in data.items():
            del elem['content']

        LOGGER.debug(data)
        return data

    def recent_data(self):
        self.gaming_machine.update()
        self.voip_machine.update()
        self.dash_machine.update()
        self.lstreaming_machine.update()
        data = {
            'last_update': self.lstreaming_machine.recent_time,
            'gaming': self.gaming_machine.state,
            'voip': self.voip_machine.state,
            'dash': self.dash_machine.state,
            'lstreaming': self.lstreaming_machine.state
        }
        
        LOGGER.debug("Collecting recent data")
        LOGGER.debug(data)
        
        return data


def parse_port():
    return '4242'

def main():
    api = NetworkUserApi()
    try:
        addr = 'tcp://127.0.0.1:' + parse_port()
        s = zerorpc.Server(api)
        s.bind(addr)
        LOGGER.debug('start running on {}'.format(addr))
        s.run()
    except:
        s.close()
    finally:
        LOGGER.debug('Exiting...')

if __name__ == '__main__':
    main()