from otree.api import (
    Page,
    WaitPage,
    models,
    widgets,
    BaseConstants,
    BaseSubsession,
    BaseGroup,
    BasePlayer,
    Currency as c,
    currency_range,
)



class Constants(BaseConstants):
    name_in_url = 'ian_public_goods_game'
    players_per_group = 3
    num_rounds = 2
    ENDOWMENT = 100
    #testing list of MPCR
    MPCR_list = [0.2, 0.4, 0.6, 0.8, 1, 1.2, 1.4, 1.6, 1.8, 2]


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    MPCR = models.FloatField()
    total_contribution = models.CurrencyField()


class Player(BasePlayer):
    contribution = models.CurrencyField(
        min=0, max=Constants.ENDOWMENT, label="How much will you contribute?"
    )


# FUNCTIONS
import random
def creating_session(subsession):
    print('in creating session')
    # Establish a total earnings variable for each participant
    # Initialize to - at beginning of session
    for p in subsession.get_players():
        if subsession.round_number == 1:
            p.participant.vars['totalEarnings'] = 0


    # Assign varying MPCR
    for g in subsession.get_groups():
        print('round', subsession.round_number)
        print('num_rounds/2', int(Constants.num_rounds/2))
        if subsession.round_number <= int(Constants.num_rounds/2):
            g.MPCR = random.choice(Constants.MPCR_list)
        else:
            g.MPCR = random.choice(Constants.MPCR_list)



def set_payoffs(g: Group):
    g.total_contribution = 0
    for p in g.get_players():
        g.total_contribution += p.contribution

    for p in g.get_players():
        print('payoff', p.participant.payoff)
        print('endowment', Constants.ENDOWMENT)
        print('contribution', p.contribution)
        print('total contribution', g.total_contribution)
        print('MPCR', g.MPCR)

        p.participant.payoff = float(Constants.ENDOWMENT - p.contribution + g.total_contribution*g.MPCR)
        p.participant.vars['totalEarnings'] += p.participant.payoff

        print('total earnings', p.participant.vars['totalEarnings'])




# PAGES
class Contribute(Page):
    form_model = 'player'
    form_fields = ['contribution']

    # def vars_for_template(player):
    #     a = 5 * 10
    #     return dict(
    #         a=a,
    #         b=1 + 1,
    #     )

class ResultsWaitPage(WaitPage):
    after_all_players_arrive = 'set_payoffs'


class Results(Page):
    pass


page_sequence = [Contribute, ResultsWaitPage, Results]
