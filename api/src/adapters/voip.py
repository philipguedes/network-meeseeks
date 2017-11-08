import collections
import os
from datetime import datetime as dt
from src.adapters import BaseAdapter
from src.utils import get_logger

BYTES_TO_MEGABITS = 128 * 1024

LOGGER = get_logger(__name__)


class VoipAdapter(BaseAdapter):
    def __init__(self):
        BaseAdapter.__init__(self)
        self.__figure = None

    @property
    def data(self):
        return self.__data

    def update_data(self):
        content = self.get_data()
        updated = dt.now()

        self.__data = {
            'content': content,
            'last_update': updated.isoformat(),
            'figure': self.get_figure()
        }

    def get_figure(self):
        if self.__figure is None:
            return self.__get_figure_updated()
        return self.__figure

    def __get_figure_updated(self):
        data = self.get_data()
        x, y = [], []

        od = collections.OrderedDict(sorted(data.items()))
        for timestamp, elem in od.items():
            x.append(dt.fromtimestamp(timestamp))
            y.append(elem['packet_loss_rate'])

        trace = self.graphics.scatter_trace(x, y)
        self.__figure = self.graphics.render_figure([trace])

        LOGGER.debug('new figure: ' + str(self.__figure))
        
        return self.__figure
        