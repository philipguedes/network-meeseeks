import collections
from datetime import datetime as dt
from src.adapters import BaseAdapter
from src.utils import get_logger


LOGGER = get_logger(__name__)


class LStreamingAdapter(BaseAdapter):
    def __init__(self):
        BaseAdapter.__init__(self)
        self.__figure = None

    @property
    def data(self):
        return self.__data

    def update_data(self):
        content = self.get_content()
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
        data = self.get_content()
        x, y = [], []

        od = collections.OrderedDict(sorted(data.items()))
        for timestamp, elem in od.items():
            x.append(dt.fromtimestamp(timestamp))
            y.append(elem['upload'])

        my_trace = self.graphics.scatter_trace(x, y, name="Upload Speed")

        layout = self.get_layout()
        traces = []
        traces.append(my_trace)

        self.__figure = self.graphics.render_figure(traces, layout=layout)

        LOGGER.debug('TODO: FIX THIS PLOT')
        LOGGER.debug('new figure: ' + str(self.__figure))

        return self.__figure

    def get_layout(self):
        kwargs = {
            'title': "Upload speed across the time",
            'titlefont': dict(
                family='Courier New, monospace',
                size=18
            ),
            'yaxis': dict(
                title='Upload speed (Megabits per second)',
                titlefont=dict(
                    family='Courier New, monospace',
                    size=18
                ),
                ticksuffix='Mbps'
            ),
            'xaxis': dict(
                title='Date',
                titlefont=dict(
                    family='Courier New, monospace',
                    size=18
                )
            )

        }
        return self.graphics.create_layout(**kwargs)