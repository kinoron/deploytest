from otree.api import *
import yaml
import random


doc = """
協力率を下げるためのパイロット実験
csv等から利得行列を読み込める仕組み必須
原型は以前演習で作ったものを利用。
"""


"""
利得行列をyamlファイルから読み込む
"""
with open('prempexp_livepage/test.yaml') as f: 
    payoff_matrix = yaml.safe_load(f)


"""
セッションを通じて固定の変数
"""
class C(BaseConstants):
    NAME_IN_URL = 'prempexp_livepage'
    PLAYERS_PER_GROUP = 2 # 参加者は2人組に分けられる
    NUM_ROUNDS = 80 # ラウンド数
    # EXP_COND = random.choice([0, 1]) #0=b2.8, 1=b1.4
    PAYOFF_MATRIX = payoff_matrix[f"round{session.config['exp_cond']}"]   # payoffmatrixを読み込む
    # PAYOFF_MATRIX = payoff_matrix
    ENDOWMENT = 50000 #500円の初期支給額
    CONTINUATION_PROB = 0.8 # ペアが継続する確率
    # CONTINUATION_PROB = [0, 0, 0, 0.1, 0.2, 0.4, 0.2, 0.1, 0, 0, 0, 0]


class Subsession(BaseSubsession):
    pass


"""
ペア（グループ）の変数の定義
"""
class Group(BaseGroup):
    
    continue_round = models.IntegerField(initial=1) # ペアの継続ラウンド数
    temp_continue_rand = models.FloatField(initial=0) # 一時的に乱数を保存する変数
    end_game = models.BooleanField(initial=False) # ペアの解散フラグ 0=続く, 1=解散する

    # max_round = models.IntegerField(initial=1)
    # def set_max_round(self):
    #     self.max_round = random.choices(
    #         [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12], 
    #         weights=C.CONTINUATION_PROB, 
    #         k=1)[0] #恣意的に定めた確率分布から、ペアが継続する回数をペア成立時に決定
        
    # def set_payoffs(self):
    #     p1, p2 = self.get_players()

    #     key1 = "round{}"
    #     key2 = "({}, {})"

    #     payoffs = C.PAYOFF_MATRIX[key1.format(self.continue_round)][key2.format(p1.decision_pd, p2.decision_pd)] # 継続ラウンドに応じて取り出す必要がある 入れ子の辞書が有力そう
    #     p1.payoff = payoffs[0]
    #     p2.payoff = payoffs[1]

    # def set_continuation(self):
    #     p1, p2 = self.get_players()

    #     if p1.decision_continue == False or p2.decision_continue == False:
    #         self.end_game = True
    #     if self.max_round == self.continue_round:
    #         self.end_game = True

    #     if self.end_game == False:
    #         self.continue_round += 1
    #         p1.player_continue_round = self.continue_round
    #         p2.player_continue_round = self.continue_round



"""
プレイヤーの変数の定義
"""
class Player(BasePlayer):
    # pdに関わる変数
    decision_pd = models.BooleanField(blank=True) # pdにおける意思決定 False=D, True=C 初期値はnone
    opponent_decision_pd = models.BooleanField(blank=True) # 相手のpdの決定
    status_pd = models.IntegerField(initial=1) # pdゲームの進行度
    timeout_pd = models.BooleanField(initial=False) # pdでタイムアウトが起こったかどうか

    # ペアの継続に関わる変数
    decision_continue = models.BooleanField() # ペアの継続における意思決定 False=no continue, True=continue 初期値はnone
    status_continue = models.IntegerField(initial = 1) # ペアの継続意思決定の進行度
    timeout_continue = models.BooleanField(initial=False) # ペアの継続意思決定でタイムアウトが起こったかどうか

    is_rematched = models.BooleanField(initial=True) # 前回ペアが解散した場合1, 継続ペアの場合0
    player_continue_round = models.IntegerField(initial=1) # 相手とペアが続いているラウンド数

    # player_max_round = models.IntegerField(initial=1)

    """
    最終成績を算出する関数
    args: player
    return: cumulative payoff
    """
    def get_cumulative_payoff(self):
        return sum([p.payoff for p in self.in_all_rounds() if p.payoff is not None]) + C.ENDOWMENT
    


"""
利得を計算する関数
args: group
returns: player.payoff
"""            
def set_payoffs(p1, p2):
    key2 = "({}, {})" # 利得構造からセルを取り出すキー
    # 入れ子の辞書からプレイヤーの利得を取り出す, livepageではnullが送信される危険性があるため、field_maybe_none
    payoffs = C.PAYOFF_MATRIX[key2.format(bool(p1.field_maybe_none('decision_pd')), bool(p2.field_maybe_none('decision_pd')))] 
    
    # プレイヤーに利得を割り当てる
    p1.payoff = payoffs[0]
    p2.payoff = payoffs[1]


"""
関係の継続を判定する関数
args: group
returns: group.end_game
"""
def set_continuation(group):
    p1, p2 = group.get_players() # 引数にとったグループから所属するプレイヤーを抽出
    p1_decision_continue = bool(p1.field_maybe_none('decision_continue')) #P1の選択, livepageではnullが送信される危険性があるため、field_maybe_none
    p2_decision_continue = bool(p2.field_maybe_none('decision_continue')) #P2の選択

    if p1_decision_continue is None or p2_decision_continue is None:
        return
    
    # もしプレイヤーのどちらかでも「継続しない」を選んだ場合、ペアは解散する
    if p1_decision_continue == False or p2_decision_continue == False:
        group.end_game = True

    # ペアが継続することになった場合、乱数が0.8より大きい値だったら(20%の確率で)ペアは解散する
    if not group.end_game  and group.temp_continue_rand == 0:
        group.temp_continue_rand = random.uniform(0, 1)
        if group.temp_continue_rand > C.CONTINUATION_PROB:
            group.end_game = True
    # if group.max_round == group.continue_round:
    #     group.end_game = True

    # if group.end_game == False:
        
    #     group.continue_round += 1
    #     p1.player_continue_round = group.continue_round
    #     p2.player_continue_round = group.continue_round


"""
グループの継続, シャッフルを判定する関数
args: subsession (全参加者情報)
return: groupmatrix
"""
def matchingsort(subsession: Subsession):

    # ラウンド1の場合はランダムマッチングを実行
    if subsession.round_number == 1:
        subsession.group_randomly()
        # for g in subsession.get_groups():
        #     g.set_max_round()
        #     g.get_players()[0].player_max_round = g.max_round
        #     g.get_players()[1].player_max_round = g.max_round
    # 再マッチング扱いにする
        for p in subsession.get_players():
            p.is_rematched = True
        #     current_group = subsession.get_groups()
        #     p.max_round_p = current_group.max_round

    # ラウンド2以降の場合は、前ラウンドの継続ペアを維持しつつ、解散ペアを再マッチング
    else:
        prev_groups = subsession.in_round(subsession.round_number - 1).get_groups()
        continued_groups = []
        rematch_pool = []

        # 前ラウンドの各グループについて、継続ペアはそのまま保持し、解散ペアは再マッチング用プールに追加
        for g in prev_groups:
            # 継続ペアの場合
            if g.end_game == False:
                # 前ラウンドのペア情報を取り出し
                current_round_players = [_.in_round(subsession.round_number) for _ in g.get_players()]
                continued_groups.append(current_round_players)
                # 継続ペアのプレイヤー情報を更新
                for p in current_round_players:
                    p.is_rematched = False
                    p.player_continue_round = p.in_round(subsession.round_number - 1).player_continue_round + 1
                    # p.player_max_round = p.in_round(subsession.round_number - 1).player_max_round

            # 解散ペアの場合
            else:
                # 再マッチング用プールにプレイヤーを追加
                current_round_players = [_.in_round(subsession.round_number) for _ in g.get_players()]
                rematch_pool.extend(current_round_players)
                # 再マッチングプレイヤーの再マッチング情報を更新
                for p in current_round_players:
                    p.is_rematched = True
        # 再マッチング用プールをシャッフルし、2人ずつ新たなペアを形成
        random.shuffle(rematch_pool)
        new_groups_matrix = [rematch_pool[i:i+2] for i in range(0, len(rematch_pool), 2)]

        # 継続ペアと新規ペアを合わせて最終的なグループマトリックスを形成
        final_matrix = continued_groups + new_groups_matrix

        # グループの構成を全体に反映
        subsession.set_group_matrix(final_matrix)

        # 各グループの継続ラウンド数を更新
        for g in subsession.get_groups():
        #     g.set_max_round()
        # プレイヤーをとってきて、そのis_rematchedの値によって処理を分岐
            sample = g.get_players()[0] 
            # 継続ペアの場合、continue_roundを前ラウンドから引き継ぐ
            if sample.is_rematched == False:
                g.continue_round = sample.player_continue_round
        #         g.max_round = sample.player_max_round
        #     else:
        #         g.get_players()[0].player_max_round = g.max_round
        #         g.get_players()[1].player_max_round = g.max_round


"""
PDのライブメソッド
args: player, 意思決定の情報
returns: dict PDの進行状況, 結果
"""
def live_method(player: Player, data):
        group = player.group
        p1, p2 = group.get_players()

        if data == {} or 'ping' in data:
            return {
                player.id_in_group: dict(
                    status_pd = player.status_pd,
                    payoff = player.payoff,
                    player_decision = player.field_maybe_none("decision_pd"),
                    opponent_decision = player.field_maybe_none("opponent_decision_pd"),
                    )
                    }

        # 意思決定が送信された場合の処理
        if 'decision_pd' in data:
            # データから意思決定を取り出し、プレイヤーに保存
            player.decision_pd = bool(data['decision_pd'])
            # pdゲームの進行状況を更新
            player.status_pd = 2

            # print(choice)
            # print("data", data)
            # print(player.decision_pd)
            # print(p1, p2)
            # print(p1.field_maybe_none("decision_pd"))

            # 両者の意思決定が揃った場合、利得計算を実行し、進行状況を更新
            if p1.field_maybe_none("decision_pd") is not None and p2.field_maybe_none("decision_pd") is not None:
                set_payoffs(p1, p2) 
                p1.opponent_decision_pd = p2.decision_pd
                p2.opponent_decision_pd = p1.decision_pd
                p1.status_pd = 3
                p2.status_pd = 3
            
        
        """
        ライブメソッドの返り値
        参加者それぞれに、PDの進行状況, 利得, 自分と相手の意思決定を返す
        参加者はこの情報をもとに、画面の表示を更新する
        """
        return {
            p.id_in_group: dict(
                status_pd = p.status_pd,
                payoff = p.payoff,
                player_decision = p.field_maybe_none("decision_pd"),
                opponent_decision = p.field_maybe_none("opponent_decision_pd"),
            )
            for p in (p1, p2)
        }
        
    

# PAGES


"""
お待ちくださいページ
"""
class Introduction(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1


"""
マッチング待ちページ
mywaitpage(5秒ごとにリフレッシュされる)
"""
class MatchingWaitPage(WaitPage):
    template_name = 'prempexp_livepage/MyWaitPage.html'
    wait_for_all_groups = True
    @staticmethod
    # 全員が到着したら、マッチングを実行
    def after_all_players_arrive(subsession: Subsession): # wait_for_all_groups = Trueなので、サブセッションの関数とする
        matchingsort(subsession)

"""
PDの相互作用ページ
60秒のタイムアウトあり
"""
class Match_Interaction(Page):
    timeout_seconds = 60
    @staticmethod
    def vars_for_template(player: Player):
        # payoffmatrixから利得を取り出す
        current_payoff_matrix = C.PAYOFF_MATRIX

        # group = player.group
        # continue_round = group.continue_round
        # key1 = "round{}"
        # current_payoff_matrix = C.PAYOFF_MATRIX[key1.format(continue_round)]

        # 利得行列の各セルをテンプレートに渡す
        return {
            'payoff_CC': current_payoff_matrix['(True, True)'],
            'payoff_CD': current_payoff_matrix['(True, False)'],
            'payoff_DC': current_payoff_matrix['(False, True)'],
            'payoff_DD': current_payoff_matrix['(False, False)'],
        }
    
    # ライブメソッド関数の呼び出し
    live_method = live_method

    # タイムアウト時の処理
    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        if timeout_happened and player.status_pd < 2:
            player.decision_pd = random.choice([True, False])
            player.timeout_pd = True

            other = player.get_others_in_group()[0]
            g = player.group
            p1, p2 = g.get_players()
            if (other.field_maybe_none('decision_pd') is not None):
                set_payoffs(p1, p2)
                if player.field_maybe_none('opponent_decision_pd') is None:
                    player.opponent_decision_pd = other.decision_pd
                if other.field_maybe_none('opponent_decision_pd') is None:
                    other.opponent_decision_pd = player.decision_pd
                player.status_pd = 3
                other.status_pd = 3

    
"""
ペアの継続意思決定ページ
60秒のタイムアウトあり
"""
class BreakUp(Page):
    timeout_seconds = 60

    """
    ペアの継続意思決定のライブメソッド
    args: player, 意思決定の情報
    returns: dict 継続意思決定の進行状況, 解散フラグ
    """
    @staticmethod
    def live_method(player: Player, data):
        group = player.group
        p1, p2 = group.get_players()

        if data == {} or 'ping' in data:
            return {
                player.id_in_group: dict(
                    status_continue = player.status_continue,
                    end_game = group.end_game,
                )
            }

        # 意思決定が送信された場合の処理
        if 'decision_continue' in data:
            print("data", data)
            # データから意思決定を取り出し、プレイヤーに保存
            player.decision_continue = bool(data['decision_continue'])
            # ペアの継続意思決定の進行状況を更新
            player.status_continue = 2

            # 両者の意思決定が揃った場合、継続判定を実行し、進行状況を更新
            if p1.field_maybe_none('decision_continue') is not None and p2.field_maybe_none('decision_continue') is not None:
                    set_continuation(group)
                    p1.status_continue = 3
                    p2.status_continue = 3
        print("status", player.status_continue)

        return {
            p.id_in_group: dict(
                status_continue = p.status_continue,
                end_game = group.end_game
                )
                for p in (p1, p2)
                }
    
    # タイムアウト時の処理
    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        if timeout_happened:
            g = player.group
            p1, p2 = g.get_players()
            player.timeout_continue = True

            if player.status_continue < 2: # まだ意思決定をしていなかった場合, ランダムに選択する
                player.decision_continue = random.choice([True, False])
                player.status_continue = 2

            other = player.get_others_in_group()[0]
            if other.field_maybe_none('decision_continue') is not None:
                set_continuation(g)
                p1.status_continue = 3
                p2.status_continue = 3


"""
最終結果ページ
"""
class FinalResults(Page):
    # 最終ラウンドでのみ表示
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == C.NUM_ROUNDS
    
    # 最終成績および謝礼額をテンプレートに渡す
    @staticmethod
    def vars_for_template(player: Player):
        return {'cumulative_payoff': player.get_cumulative_payoff(),
                'final_pay': 2500 + (player.get_cumulative_payoff()).to_real_world_currency(player.session)
                }


page_sequence = [
    Introduction, 
    MatchingWaitPage,
    Match_Interaction,
    BreakUp,
    FinalResults,
]
