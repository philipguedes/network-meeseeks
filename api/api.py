from __future__ import print_function
import sys
import zerorpc
from src.adapters.voip import VoipAdapter


class NetworkUserApi(object):
    """
    Translate the network tests result in a way
    more user friendly.
    """
    def __init__(self):
        self.graph_creator = None
        self.voip_adapter = VoipAdapter()

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

        It considers mostly the packet loss and the download/upload speed.
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
        return self.voip_adapter.data

    def update_graphic(self):
        pass
    

def parse_port():
    return '4242'

def main():
    addr = 'tcp://127.0.0.1:' + parse_port()
    s = zerorpc.Server(NetworkUserApi())
    s.bind(addr)
    print('start running on {}'.format(addr))
    s.run()

if __name__ == '__main__':
    main()