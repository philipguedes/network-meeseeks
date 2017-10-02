import math
from src.services.neubot import NeubotService


C = 0.93
MSS = 1460

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

    def packet_loss(self, goodput, rtt):
        """
        Uses mathis equation to estimate packet loss
        """
        den = goodput * rtt
        num = C * MSS
        plr_sqrt = num/den
        plr = math.pow(plr_sqrt, 2)
        return plr


