from transitions import Machine, State
from src.adapters.lstreaming import LStreamingAdapter


LS_STATES = {
    "0": "error=1",
    "A": "freeze=1",
    "B": "1440=1",
    "C": "1080=1",
    "D": "720=1",
    "E": "480=1",
    "F": "360=1",
    "G": "240=1"
}

class LStreamingStateMachine(object):
    """
    Provides a translation to collected data
    to present to the user.
    """
    
    states = list(LS_STATES.values())
    
    transitions = [
        {'trigger': 'update',
            'source': '*',
            'dest': VOIP_STATES['A'],
            'conditions': ['freeze']},
        {'trigger': 'update',
            'source': '*',
            'dest': VOIP_STATES['B'],
            'conditions': ['up_to_1440']},
        {'trigger': 'update',
            'source': '*',
            'dest': VOIP_STATES['C'],
            'conditions': ['up_to_1080'],
            'unless': [
                'freeze',
                'up_to_1440']},
        {'trigger': 'update',
            'source': '*',
            'dest': VOIP_STATES['D'],
            'conditions': ['up_to_720'],
            'unless': [
                'freeze'
                'up_to_1080']},
        {'trigger': 'update',
            'source': '*',
            'dest': VOIP_STATES['E'],
            'conditions': ['up_to_480'],
            'unless': [
                'freeze'
                'up_to_720']},
        {'trigger': 'update',
            'source': '*',
            'dest': VOIP_STATES['F'],
            'conditions': ['up_to_360'],
            'unless': [
                'up_to_480,
                'freeze']},
        {'trigger': 'update',
            'source': '*',
            'dest': VOIP_STATES['G'],
            'conditions': ['up_to_240'],
            'unless': [
                'freeze',
                'up_to_360']},
    ]
    
    def __init__(self):
        self.machine = Machine(
            model=self,
            states=LStreamingStateMachine.states,
            transitions=LStreamingStateMachine.transitions,
            prepare_event='measure',
            initial='0')
        self.adapter = LStreamingAdapter()

    def measure(self):
        """
        Get recent data
        """
        self.recent_time, self.recent_data = self.adapter.get_recent_data()
        print('Measuring...')

    def freeze(self):
        """
        Returns True if PLR > 1%
        """
        return self.recent_data['packet_loss_rate'] > 0.01:

    def up_to_1440(self):
        """
        This state machine follows the youtube guideline for streaming bitrates

        https://support.google.com/youtube/answer/2853702?hl=en&ref_topic=6136989
        """
        # TODO: convert to upload speed to kbps
        return self.recent_data['upload'] >= 18000

    def up_to_1080(self):
        return self.recent_data['upload'] >= 9000

    def up_to_720(self):
        return self.recent_data['upload'] >= 4000

    def up_to_480(self):
        return self.recent_data['upload'] >= 2000

    def up_to_360(self):
        return self.recent_data['upload'] >= 1000

    def up_to_240(self):
        return self.recent_data['upload'] > 700