import os
import tempfile
import plotly.offline as py
import plotly.graph_objs as go

CURRENT_DIR = os.getcwd()

# TODO: resolve path
DIST_FOLDER = os.getenv('RESOURCES_FOLDER', '/home/philip/dev/network-meeseeks/res')


class GraphicsService(object):
    def __init__(self):
        self.__file = None

    @property
    def name(self):
        return self.__file.name if self.__file is not None else None

    def scatter_trace(self, x_axis, y_axis, **kwargs):
        name = kwargs.get('name', '')
        connectgaps = kwargs.get('connectgaps', True)

        trace = go.Scatter(
            x=x_axis,
            y=y_axis,
            name=name,
            connectgaps=connectgaps)
        
        return trace

    def create_tempfile(self):
        self.__file = tempfile.NamedTemporaryFile(delete=True, suffix='.html')
        return self.name
    
    def render_figure(self, traces):
        filename = self.create_tempfile()
        figure = dict(data=traces)

        path = py.plot(
            figure, 
            filename=filename, 
            auto_open=False,
            image_height=480,
            image_width=640)

        return path


