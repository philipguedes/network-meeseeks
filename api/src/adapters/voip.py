import collections
from datetime import datetime as dt
from src.adapters import BaseAdapter


BYTES_TO_MEGABITS = 128 * 1024


class VoipAdapter(BaseAdapter):
    def __init__(self):
        BaseAdapter.__init__(self)
        self.__data = None

    @property
    def data(self):
        return self.__data

    def update_data(self):
        content = self.get_data()
        # updated = arrow.utcnow().timestamp
        updated = None

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

    def get_recent_data(self):
        data = self.get_data()
        most_recent = max(data, key=int)
        return most_recent, data[most_recent]

    def update_plot(self):
        data = self.get_data()
        x = []
        y = []

        od = collections.OrderedDict(sorted(data.items()))
        for timestamp, elem in od.items():
            x.append(dt.fromtimestamp(timestamp))
            y.append(elem['goodput']/BYTES_TO_MEGABITS)

        trace = self.graphics.scatter_trace(x, y)
        path = self.graphics.render_figure([trace], 'voip')
        print('done')
        return path