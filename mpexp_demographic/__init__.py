from otree.api import *


doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'mpexp_demographic'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


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
    age = models.IntegerField(label="")
    gender = models.StringField(
        choices=["男性", "女性", "その他", "回答したくない"],
        widget=widgets.RadioSelect,
        label="",
    )
    svoA1 = make_field("svoA1")
    svoA2 = make_field("svoA2")
    svoA3 = make_field("svoA3")
    svoA4 = make_field("svoA4")
    svoA5 = make_field("svoA5")
    svoA6 = make_field("svoA6")
    svoA7 = make_field("svoA7")
    svoA8 = make_field("svoA8")
    svoA9 = make_field("svoA9")
    svoA10 = make_field("svoA10")
    svoA11 = make_field("svoA11")
    svoA12 = make_field("svoA12")
    svoA13 = make_field("svoA13")
    svoA14 = make_field("svoA14")
    svoA15 = make_field("svoA15")



# PAGES
class Survey(Page):
    form_model = 'player'
    form_fields = ['age', 'gender', 'svoA1', 'svoA2', 'svoA3', 'svoA4', 'svoA5',
                  'svoA6']



class Results(Page):
    @staticmethod
    def vars_for_template(player: Player):
        return {
            'totalpayoff_ingame': player.participant.cumulative_payoff,
            'finalpay_inreal': 2500 + (player.participant.cumulative_payoff).to_real_world_currency(player.session)
        }


page_sequence = [Survey, Results]
