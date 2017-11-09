import collections
from datetime import datetime as dt
from src.adapters import BaseAdapter
from src.utils import get_logger

LOGGER = get_logger(__name__)


class VoipAdapter(BaseAdapter):
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
            'content_update': updated.isoformat(),
            'figure_update': updated.isoformat(),
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
            y.append(1000*elem['latency'])
            
        my_trace = self.graphics.scatter_trace(x, y, name="Latency")

        layout = self.get_layout()
        traces = self.__get_standard_traces(x)
        traces.append(my_trace)

        self.__figure = self.graphics.render_figure(traces, layout=layout)
        self.__last_update = dt.now()

        LOGGER.debug('TODO: FIX THIS PLOT')
        LOGGER.debug('new figure: ' + str(self.__figure))
        
        return self.__figure    

    def __get_clean_area(self, x):
        y = [300 for date in x]
        kwargs = dict(
            name="Zone without delay",
            fill="tozeroy",
            fillcolor="#E3F2FD",
            line={'width': 0.5}
        )
        return self.graphics.scatter_trace(x, y, **kwargs)

    # def __get_area(self, x):
    #     y = [100 for date in x]
    #     kwargs = dict(
    #         name="Freeze Zone",
    #         fill="tozeroy",
    #         fillcolor="#E3F2FD",
    #         line={'width': 0.5}
    #     )
    #     return self.graphics.scatter_trace(x, y, **kwargs)

    def __get_standard_traces(self, x):
        trace1 = self.__get_clean_area(x)
        # trace2 = self.__get_area(x)
        return [trace1]

    def get_layout(self):
        kwargs = {
            'title': "Latency across the time",
            'titlefont': dict(
                family='Courier New, monospace',
                size=18
            ),
            'yaxis': dict(
                title='Latency (millisecond)',
                titlefont=dict(
                    family='Courier New, monospace',
                    size=18
                ),
                # type='-',
                # range=[0, 100.0],
                ticksuffix='ms'
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