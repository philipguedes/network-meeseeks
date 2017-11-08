import os
import math
from src.services.neubot import NeubotService
from src.services.graphics import GraphicsService


C = os.getenv('C_CONSTANT', 0.93)
MSS = os.getenv('MSS_CONSTANT', 1460)


class BaseAdapter(object):
    """
    This class provides methods to work with the services module 
    """

    def __new__(cls, *args, **kwargs):
        """
        BaseAdapter provides common methods to its subclasses.
        This class may not be instantiated at all.
        """
        if cls is BaseAdapter:
            raise TypeError("BaseAdapter class may not be instantiated")
        return object.__new__(cls, *args, **kwargs)
    
    def __init__(self):
        self.service = NeubotService()
        self.graphics = GraphicsService()
        self.__data = None
        self.__figure = None

    def get_data(self):
        data = self.service.speedtest_data()
        for _, elem in data.items():
            goodput = elem['goodput']
            rtt = elem['rtt']
            plr = self.packet_loss(goodput, rtt)
            elem['packet_loss_rate'] = plr
        return data

    def get_recent_data(self):
        data = self.get_data()
        most_recent = max(data, key=int)
        return most_recent, data[most_recent]

    def packet_loss(self, goodput, rtt):
        """
        Uses mathis equation to estimate packet loss
        """
        den = goodput * rtt
        num = C * MSS
        plr_sqrt = num/den
        plr = math.pow(plr_sqrt, 2)
        return plr

    def __exit__(self, exc_type, exc_value, traceback):
        try:
            if self.__figure is not None:
                os.unlink(self.__figure)
                print("CLEANED FIGURE")
            
        except:
            print('CANT UNLINK FIGURE IN EXIT: ' + str(self.__figure))
            pass

    def __del__(self):
        try:
            if self.__figure is not None:
                os.unlink(self.__figure)
                print("CLEANED FIGURE")
        except:
            print('CANT UNLINK FIGURE IN DEL: ' + str(self.__figure))
            pass