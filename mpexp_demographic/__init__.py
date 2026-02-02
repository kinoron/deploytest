from otree.api import *


doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'mpexp_demographic'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 6


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass

def make_field(label):
    return models.IntegerField(
        choices = [1,2,3,4,5,6,7,8,9],
        widget = widgets.RadioSelect,
        label=label,
    )

class Player(BasePlayer):
    # 1-15のフィールドを追加（choices)
    age = models.IntegerField(label="半角数字でお答えください", min=18, max=120)
    gender = models.StringField(
        choices=["男性", "女性", "その他", "回答したくない"],
        widget=widgets.RadioSelect,
        label="",
    )
    svoA = models.IntegerField(
        choices = [1,2,3,4,5,6,7,8,9],
        widget = widgets.RadioSelect,
    )
    # svoA7 = make_field("svoA7")
    # svoA8 = make_field("svoA8")
    # svoA9 = make_field("svoA9")
    # svoA10 = make_field("svoA10")
    # svoA11 = make_field("svoA11")
    # svoA12 = make_field("svoA12")
    # svoA13 = make_field("svoA13")
    # svoA14 = make_field("svoA14")
    # svoA15 = make_field("svoA15")



# PAGES
class Survey(Page):
    form_model = 'player'
    form_fields = ['age', 'gender']
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1

class SVO(Page):
    form_model = 'player'
    form_fields = ['svoA']

class Results(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 6
    @staticmethod
    def vars_for_template(player: Player):
        return {
            'totalpayoff_ingame': player.participant.cumulative_payoff,
            'totalpayoff_inreal': (player.participant.cumulative_payoff).to_real_world_currency(player.session),
            'finalpay_inreal': 2500 + (player.participant.cumulative_payoff).to_real_world_currency(player.session)
        }


page_sequence = [Survey, SVO, Results]
