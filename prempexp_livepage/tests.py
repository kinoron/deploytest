from otree.api import Currency as C, currency_range, expect, Bot
from . import *

def call_live_method(method, **kwargs):
    if page_class == pages.Match_Interaction:
        method(1, {'decision_pd': random.choice([0, 1])})
        method(2, {'decision_pd': random.choice([0, 1])})
        yield Match_Interaction
    
    if page_class == pages.BreakUp:
        method(1, {'decision_continue': random.choice([0, 1])})
        method(2, {'decision_continue': random.choice([0, 1])})
        yield BreakUp


class PlayerBot(Bot):

    def play_round(self):
        if self.round_number == 1: 
            yield Introduction

