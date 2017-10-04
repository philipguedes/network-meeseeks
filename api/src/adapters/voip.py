import arrow
from src.adapters import BaseAdapter


class VoipAdapter(BaseAdapter):
    def __init__(self):
        BaseAdapter.__init__(self)
        self.__data = None

    @property
    def data(self):
        return self.__data

    def update_data(self):
        
        content = self.get_data()
        updated = arrow.utcnow().timestamp

        self.__data = {
            'content': content,
            'last_update': updated
        }

    def get_data(self):
        data = self.service.speedtest_data()
        for _,elem in data.items():
            goodput = elem['goodput']
            rtt = elem['rtt']
            plr = self.packet_loss(goodput, rtt)
            elem['packet_loss_rate'] = plr

        return data

        

    