from otree.api import *


doc = """
introduction for prempexp
"""


class C(BaseConstants):
    NAME_IN_URL = 'prempexp_introduction'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    q1 = models.IntegerField(choices=[
        [1, '600point'],
        [2, '400point'],
        [3, '-200point'],
        [4, '0point'],],
        widget=widgets.RadioSelect,
        label=""
    )

    q2 = models.BooleanField(choices=[[False, '次のラウンドも同じ相手と取引が続く'], 
                                      [True, '次のラウンドは違う相手と新しく取引を始める']],
                                      label="")
    q3 = models.BooleanField(choices=[[False, '必ず同じ相手と取引が続く'],
                                      [True, '小さな確率で、関係が解消することがある']],
                                      label="")


# PAGES
class Consent(Page):
    pass


class Comprehension(Page):
    form_model = 'player'
    form_fields = ['q1', 'q2', 'q3']

    @staticmethod
    def error_message(player: Player, values):
        solutions = dict(
            q1 = 3,
            q2 = True,
            q3 = True,    
        )

        error_messages = dict()
        for field_name in solutions:
            if values[field_name] != solutions[field_name]:
                error_messages[field_name] = "正しい答えを入力してください"
        
        return error_messages


page_sequence = [Consent, Comprehension]
