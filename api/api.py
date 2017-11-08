from __future__ import print_function
import sys
import zerorpc
import json
import tempfile
from src.adapters.voip import VoipAdapter
from src.machines.dash import DashStateMachine
from src.machines.voip import VoipStateMachine
from src.machines.gaming import GamingStateMachine
from src.machines.lstreaming import LStreamingStateMachine

class NetworkUserApi(object):
    """
    Translate the network tests result in a way
    more user-friendly.
    """
    def __init__(self):
        self.graph_creator = None
        self.__initialize_machines()
        self.voip_adapter = self.voip_machine.adapter

    def __initialize_machines(self):
        self.voip_machine = VoipStateMachine()
        self.dash_machine = DashStateMachine()
        self.gaming_machine = GamingStateMachine()
        self.lstreaming_machine = LStreamingStateMachine()

    def dash(self):
        """
        Translate parameters related to Dynamic Adaptive Streaming 
        over HTTP (DASH).
        It uses Netflix and Youtube as an example

        It considers mostly the bandwidth (for video quality) | download speed.
        """
        pass

    def streaming(self):
        """
        Translate parameters related to HTTP Live Streaming (HLS)
        It uses Twitch and Youtube as an example

        It considers mostly the packet loss and the upload speed.
        """
        pass

    def gamming(self):
        """
        Translate parameters related to Gamming.
        It uses League of Legends and Dota2 as an example

        It considers mostly the packet loss.
        It should consider either the human reaction time.
        """
        pass

    def voip(self):
        """
        Translate parameters related to Voip services.
        It uses Skype, Discord and Hangouts as an example.

        If using only audio, it should consider the packet loss.
        If using video too, it should consider the bandwidth also.
        """
        self.voip_adapter.update_data()
        return json.dumps(self.voip_adapter.data)

    def update_graphic(self):
        return "Olá professora! Esta funcionalidade ainda não está implementada, mas logo estará :)"
    
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
        print(data)
        return data


def parse_port():
    return '4242'

def main():
    api = NetworkUserApi()
    try:
        addr = 'tcp://127.0.0.1:' + parse_port()
        s = zerorpc.Server(api)
        s.bind(addr)
        print('start running on {}'.format(addr))
        s.run()
    except:
        s.close()
    finally:
        print('Exiting...')

if __name__ == '__main__':
    main()