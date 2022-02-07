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
    MPCR1 = 0.5
    MPCR2 = 1.5


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    MPCR = models.FloatField()
    total_contribution = models.CurrencyField()
    individual_share = models.CurrencyField()


class Player(BasePlayer):
    contribution = models.CurrencyField(
        min=0, max=Constants.ENDOWMENT, label="How much will you contribute?"
    )


# FUNCTIONS
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
            g.MPCR = Constants.MPCR1
        else:
            g.MPCR = Constants.MPCR2


def set_payoffs(g: Group):
    players = g.get_players()
    contributions = [p.contribution for p in players]
    g.total_contribution = sum(contributions)
    g.individual_share = (
        g.total_contribution * g.MPCR / Constants.players_per_group
    )
    for p in players:
        p.payoff = Constants.ENDOWMENT - p.contribution + g.individual_share
        p.participant.vars['totalEarnings'] += p.payoff
        print('payoff', p.participant.payoff)
        print('endowment', Constants.ENDOWMENT)
        print('contribution', p.contribution)
        print('total contribution', g.total_contribution)
        print('MPCR', g.MPCR)
        print('total earnings', p.participant.vars['totalEarnings'])


# PAGES
class Contribute(Page):
    form_model = 'player'
    form_fields = ['contribution']


class ResultsWaitPage(WaitPage):
    after_all_players_arrive = set_payoffs


class Results(Page):
    pass


page_sequence = [Contribute, ResultsWaitPage, Results]
