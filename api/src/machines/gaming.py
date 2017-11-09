from transitions import Machine, State
from src.adapters.gaming import GamingAdapter
from src.utils import get_logger


LOGGER = get_logger(__name__)

GAMING_STATES = {
    "0": "error",
    "A": "freeze",
    "B": "latency",
    "C": "freeze&latency",
    "D": "ok"
}

class GamingStateMachine(object):
    """
    Provides a translation to collected data
    to present to the user.
    """
    
    states = list(GAMING_STATES.values())
    
    transitions = [
        {'trigger': 'update',
            'source': '*',
            'dest': GAMING_STATES['A'],
            'conditions': ['freeze']},
        {'trigger': 'update',
            'source': '*',
            'dest': GAMING_STATES['B'],
            'conditions': ['latency']},
        {'trigger': 'update',
            'source': '*',
            'dest': GAMING_STATES['C'],
            'conditions': ['freeze', 'latency']},
        {'trigger': 'update',
            'source': '*',
            'dest': GAMING_STATES['D'],
            'unless': [
                'latency',
                'freeze']}
    ]
    
    def __init__(self):
        self.machine = Machine(
            model=self,
            states=GamingStateMachine.states,
            transitions=GamingStateMachine.transitions,
            prepare_event='measure',
            initial='0')
        self.adapter = GamingAdapter()

    def measure(self):
        """
        Get recent data
        """
        self.recent_time, self.recent_data = self.adapter.get_recent_content()
        self.compute_statistics()
        LOGGER.debug('Measuring...')

    def compute_statistics(self):
        data = self.adapter.get_content()
        acc = 0
        for _,elem in data.items():
            acc += elem['latency']
        self.mean_latency = acc/len(data)

    def freeze(self):
        """
        Returns True if PLR > 10%
        """
        return self.recent_data['packet_loss_rate'] > 0.1

    def latency(self):
        """
        """
        return self.recent_data['latency'] > (1.1 * self.mean_latency)