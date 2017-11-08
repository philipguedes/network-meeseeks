import collections
from datetime import datetime as dt
from src.adapters import BaseAdapter


BYTES_TO_MEGABITS = 128 * 1024 


class GamingAdapter(BaseAdapter):
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

    def update_plot(self):
        # TODO: fix this
        data = self.get_data()
        x = []
        y = []
        
        od = collections.OrderedDict(sorted(data.items()))
        for timestamp, elem in od.items():
            x.append(dt.fromtimestamp(timestamp))
            y.append(elem['goodput']/BYTES_TO_MEGABITS)
        
        trace = self.graphics.scatter_trace(x, y)
        path = self.graphics.render_figure([trace])
        print('done')
        return path