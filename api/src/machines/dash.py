from transitions import Machine, State
from src.adapters.dash import DashAdapter
from src.utils import get_logger


LOGGER = get_logger(__name__)

DASH_STATES = {
    "0": "error",
    "A": "impossible",
    "B": "minimum",
    "C": "recommended",
    "D": "sd",
    "E": "hd",
    "F": "ultra"
}

class DashStateMachine(object):
    """
    Provides a translation to collected data
    to present to the user.
    """
    
    states = list(DASH_STATES.values())
    
    transitions = [
        {'trigger': 'update',
            'source': '*',
            'dest': DASH_STATES['A'],
            'conditions': ['less_than_minimum']},
        {'trigger': 'update',
            'source': '*',
            'dest': DASH_STATES['B'],
            'conditions': ['minimum'],
            'unless': ['recommended']},
        {'trigger': 'update',
            'source': '*',
            'dest': DASH_STATES['C'],
            'conditions': ['recommended'],
            'unless': ['sd']},
        {'trigger': 'update',
            'source': '*',
            'dest': DASH_STATES['D'],
            'conditions': ['sd'],
            'unless': ['hd']},
        {'trigger': 'update',
            'source': '*',
            'dest': DASH_STATES['E'],
            'conditions': ['hd'],
            'unless': ['ultra']},
        {'trigger': 'update',
            'source': '*',
            'dest': DASH_STATES['F'],
            'conditions': ['ultra']}
    ]
    
    def __init__(self):
        self.machine = Machine(
            model=self,
            states=DashStateMachine.states,
            transitions=DashStateMachine.transitions,
            prepare_event='measure',
            initial='0')
        self.adapter = DashAdapter()

    def measure(self):
        """
        Get recent data
        """
        self.recent_time, self.recent_data = self.adapter.get_recent_content()
        LOGGER.debug('Measuring...')

    def less_than_minimum(self):
        """
        This state machine follows the Netflix requirements

        The numbers are currently in Mbps

        https://help.netflix.com/en/node/306
        """
        return self.recent_data['goodput'] < 0.5

    def minimum(self):
        return self.recent_data['goodput'] >= 0.5

    def recommended(self):
        return self.recent_data['goodput'] >= 1.5

    def sd(self):
        return self.recent_data['goodput'] >= 3.0

    def hd(self):
        return self.recent_data['goodput'] >= 5.0

    def ultra(self):
        return self.recent_data['goodput'] >= 25