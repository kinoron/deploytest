from otree.api import *


doc = """
実験同意および理解度確認チェック
"""


class C(BaseConstants):
    NAME_IN_URL = 'mpexp_introduction'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    q1 = models.BooleanField(choices=[[True, '○'],
                                      [False, '×'],],
                                      label=""
                                      )

    q2 = models.IntegerField(choices=[
        [1, '700point'],
        [2, '450point'],
        [3, '-250point'],
        [4, '0point'],],
        widget=widgets.RadioSelect,
        label=""
    )

    q3 = models.BooleanField(choices=[[False, '次のラウンドも同じ相手と取引が続く'], 
                                      [True, '次のラウンドは違う相手と新しく取引を始める']],
                                      label="")
    
    q4 = models.BooleanField(choices=[[False, '必ず同じ相手と取引が続く'],
                                      [True, '基本的に同じ相手との関係が継続するが、小さい確率で関係が解消することがある']],
                                      label="")


# PAGES
class Consent(Page):
    pass


class Comprehension(Page):
    form_model = 'player'
    form_fields = ['q1', 'q2', 'q3', 'q4']

    @staticmethod
    def error_message(player: Player, values):
        solutions = dict(
            q1 = False,
            q2 = 3,
            q3 = True,    
            q4 = True,
        )

        error_messages = dict()
        for field_name in solutions:
            if values[field_name] != solutions[field_name]:
                error_messages[field_name] = "正しい答えを入力してください"
        
        return error_messages


page_sequence = [Consent, Comprehension]
