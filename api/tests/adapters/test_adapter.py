import pytest
import operator
import math
from functools import reduce
from src.services.neubot import NeubotService
from src.adapters import BaseAdapter
from src.adapters import MSS, C


class CommonAdapter(BaseAdapter):
    def __init__(self):
        BaseAdapter.__init__(self)


@pytest.fixture(scope='module')
def common_adapter():
    return CommonAdapter()


class TestBaseAdapter(object):
    @property
    def const(self):
        return reduce(operator.mul, map(lambda x: math.pow(x, 2), [MSS, C]))

    def test_wrong_instantiation(self):
        with pytest.raises(TypeError) as te:
            my_class = BaseAdapter()

    def test_inheritance(self, common_adapter):
        assert type(common_adapter.service) is NeubotService

    def test_packet_loss(self, common_adapter):
        goodput = [0.3245, 0.666, 4.2]
        rtt = [0.554, 0.5123, 1.234]
        results = [30.9421914031, 8.59019118943, 0.03722811954]

        with pytest.raises(Exception):
            common_adapter.packet_loss(0, 10)
        
        with pytest.raises(Exception):
            common_adapter.packet_loss(10, 0)

        result_0 = common_adapter.packet_loss(goodput[0], rtt[0])/self.const
        result_1 = common_adapter.packet_loss(goodput[1], rtt[1])/self.const
        result_2 = common_adapter.packet_loss(goodput[2], rtt[2])/self.const

        assert math.isclose(result_0, results[0], abs_tol=0.05)
        assert math.isclose(result_1, results[1], abs_tol=0.05)
        assert math.isclose(result_2, results[2], abs_tol=0.05)
    
    def test_something(self, common_adapter):
        pass
