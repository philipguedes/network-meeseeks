from transitions import Machine, State
from src.adapters.voip import VoipAdapter


VOIP_STATES = {
    "0": "error=1",
    "A": "freeze=1",
    "B": "delay=1",
    "C": "connect_issue=1",
    "D": "freeze=1&delay=1",
    "E": "freeze=1&connect_issue=1",
    "F": "delay=1&connect_issue=1",
    "G": "freeze=1&delay=1&connect_issue=1",
    "H": ""
}

class VoipStateMachine(object):
    """
    Provides a translation to collected data
    to present to the user.
    """
    
    states = list(VOIP_STATES.values())
    
    transitions = [
        {'trigger': 'update',
            'source': '*',
            'dest': VOIP_STATES['A'],
            'conditions': ['freeze']},
        {'trigger': 'update',
            'source': '*',
            'dest': VOIP_STATES['B'],
            'conditions': ['delay']},
        {'trigger': 'update',
            'source': '*',
            'dest': VOIP_STATES['C'],
            'conditions': ['connect_issue']},
        {'trigger': 'update',
            'source': '*',
            'dest': VOIP_STATES['D'],
            'conditions': [
                'freeze',
                'delay']},
        {'trigger': 'update',
            'source': '*',
            'dest': VOIP_STATES['E'],
            'conditions': [
                'freeze',
                'connect_issue']},
        {'trigger': 'update',
            'source': '*',
            'dest': VOIP_STATES['F'],
            'conditions': [
                'connect_issue',
                'delay']},
        {'trigger': 'update',
            'source': '*',
            'dest': VOIP_STATES['G'],
            'conditions': [
                'freeze',
                'delay',
                'connect_issue']},
        {'trigger': 'update',
            'source': '*',
            'dest': VOIP_STATES['H'],
            'unless': [
                'freeze',
                'delay',
                'connect_issue']}
    ]
    
    def __init__(self):
        self.machine = Machine(
            model=self,
            states=VoipStateMachine.states,
            transitions=VoipStateMachine.transitions,
            prepare_event='measure',
            initial='0')
        self.adapter = VoipAdapter()

    def measure(self):
        """
        Latencia> atraso
        PLR > erros
        largura de banda > 100kbps
        download > 100kbps
        upload > 100 kbps
        """
        self.recent_time, self.recent_data = self.adapter.get_recent_data()
        print('Measuring...')

    def freeze(self):
        """
        Returns True if PLR > 1%
        """
        return self.recent_data['packet_loss_rate'] > 0.01:

    def delay(self):
        """
        Returns True if latency > 300ms
        """
        return self.recent_data['latency'] > 300

    def connect_issues(self):
        """
        Returns True if bandwidth (upload/download) < 100kbps (convert to kbps)
        """
        return self.recent_data['goodput'] < 100