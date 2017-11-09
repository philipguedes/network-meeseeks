import collections
from datetime import datetime as dt
from src.adapters import BaseAdapter
from src.utils import get_logger

LOGGER = get_logger(__name__)
BYTES_TO_MEGABITS = 128 * 1024


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
            if elem['packet_loss_rate'] <= 1.0:
                x.append(dt.fromtimestamp(timestamp))
                y.append(100*elem['packet_loss_rate'])

            else:
                LOGGER.error('Error for data?\n timestamp: {}, elem: {}'.format(timestamp, elem))
        my_trace = self.graphics.scatter_trace(x, y, name="Packet Loss")

        layout = self.get_layout()
        traces = self.__get_standard_traces(x)
        traces.append(my_trace)

        self.__figure = self.graphics.render_figure(traces, layout=layout)

        LOGGER.debug('TODO: FIX THIS PLOT')
        LOGGER.debug('new figure: ' + str(self.__figure))
        
        return self.__figure    

    def __get_clean_area(self, x):
        y = [1 for date in x]
        kwargs = dict(
            name="Clean Zone",
            fill="tozeroy",
            fillcolor="#FFEBEE",
            line={'width': 0.5}
        )
        return self.graphics.scatter_trace(x, y, **kwargs)

    def __get_area(self, x):
        y = [100 for date in x]
        kwargs = dict(
            name="Freeze Zone",
            fill="tozeroy",
            fillcolor="#E3F2FD",
            line={'width': 0.5}
        )
        return self.graphics.scatter_trace(x, y, **kwargs)

    def __get_standard_traces(self, x):
        trace1 = self.__get_clean_area(x)
        trace2 = self.__get_area(x)
        return [trace2, trace1]

    def get_layout(self):
        kwargs = {
            'title': "Packet loss percentage across the time",
            'titlefont': dict(
                family='Courier New, monospace',
                size=18
            ),
            'yaxis': dict(
                title='Packet Loss %',
                titlefont=dict(
                    family='Courier New, monospace',
                    size=18
                ),
                type='-',
                range=[0, 100.0],
                ticksuffix='%',
                tickformat=".2f"
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