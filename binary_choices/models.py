import random
from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
from binary_choices.config import *
from binary_choices.backend.shared_info import *
import binary_choices.backend.bisection_engine as q_engine


author = 'Nicolò Bertani'

doc = """
This is decription of the binary_choices app.
"""


# ******************************************************************************************************************** #
# *** CLASS SUBSESSION
# ******************************************************************************************************************** #
class Subsession(BaseSubsession):

    # initiate list of sure payoffs and implied switching row in first round
    # ------------------------------------------------------------------------------------------------------------
    def creating_session(self):
        
        if self.round_number == 1:
            for i, p in enumerate(self.get_players()):

                p.participant.vars.update({
                    'experimental_design' : [i], #incomplete
                    'winning_participant' : random.random() < share_winners,
                    'last_q' : False,
                    'large_opt_first' : random.choice([True, False]),
                })
        
        self.session.vars['num_rounds'] = Constants.num_rounds


# ******************************************************************************************************************** #
# *** CLASS GROUP
# ******************************************************************************************************************** #
class Group(BaseGroup):
    pass


# ******************************************************************************************************************** #
# *** CLASS PLAYER
# ******************************************************************************************************************** #
class Player(BasePlayer):

    # add model fields to class player
    # ----------------------------------------------------------------------------------------------------------------

    # player model
    player_model = q_engine.Bisection()
    
    # records
    ## choices
    ### practice
    practice_choice = models.BooleanField()
    comp_q1 = models.StringField()
    comp_q2 = models.StringField()

    ### main
    p_x = models.FloatField()
    z = models.FloatField()
    choice = models.StringField()
    s = models.BooleanField()
    
    # timestamps
    instruction_timestamp = models.StringField()
    practice_timestamp = models.StringField()
    comp_timestamp = models.StringField()
    intro_timestamp = models.StringField()
    q_timestamp = models.StringField()
    end_timestamp = models.StringField()

    # payoffs
    winning_participant = models.BooleanField()
    winning_choice = models.IntegerField()
    
    # old
    switching_row = models.IntegerField()
    random_draw = models.IntegerField()
    payoff_relevant = models.StringField()
    sure_payoff = models.FloatField()

    # set sure payoff for next choice
    # ----------------------------------------------------------------------------------------------------------------
    def set_sure_payoffs(self):

        # add current round's sure payoff to model field
        # ------------------------------------------------------------------------------------------------------------
        self.sure_payoff = float(self.participant.vars['icl_sure_payoffs'][self.round_number - 1])

        # determine sure payoff for next choice and append list of sure payoffs
        # ------------------------------------------------------------------------------------------------------------
        if not self.round_number == Constants.num_choices:

            if self.choice == 'lottery':
                next_sure_payoff = self.participant.vars['icl_sure_payoffs'][self.round_number - 1] + Constants.delta / 2 ** (self.round_number - 1)
            elif self.choice == 'sure_amount':
                next_sure_payoff = self.participant.vars['icl_sure_payoffs'][self.round_number - 1] - Constants.delta / 2 ** (self.round_number - 1)

            self.participant.vars['icl_sure_payoffs'].append(float(next_sure_payoff))

    # update implied switching row each round
    # ----------------------------------------------------------------------------------------------------------------
    def update_switching_row(self):

        if self.choice == 'sure_amount':
            self.participant.vars['icl_switching_row'] -= 2 ** (Constants.num_choices - self.round_number)

    # set payoffs
    # ----------------------------------------------------------------------------------------------------------------
    def set_payoffs(self):

        current_round = self.subsession.round_number
        current_choice = self.in_round(current_round).choice

        # set payoff if all choices have been completed
        # ------------------------------------------------------------------------------------------------------------
        if current_round == Constants.num_rounds:

            # randomly determine which choice to pay
            # --------------------------------------------------------------------------------------------------------
            completed_choices = len(self.participant.vars['icl_sure_payoffs'])
            self.participant.vars['icl_choice_to_pay'] = random.randint(1, completed_choices)
            choice_to_pay = self.participant.vars['icl_choice_to_pay']

            # random draw to determine whether to pay the "high" or "low" lottery outcome
            # --------------------------------------------------------------------------------------------------------
            self.in_round(choice_to_pay).random_draw = random.randint(1, 100)

            # determine whether the lottery or sure payoff is relevant for payment
            # --------------------------------------------------------------------------------------------------------
            self.in_round(choice_to_pay).payoff_relevant = self.in_round(choice_to_pay).choice

            # set player's payoff
            # --------------------------------------------------------------------------------------------------------
            if self.in_round(choice_to_pay).payoff_relevant == 'lottery':
                self.in_round(choice_to_pay).payoff = Constants.lottery_hi \
                    if self.in_round(choice_to_pay).random_draw <= Constants.probability \
                    else Constants.lottery_lo
            elif self.in_round(choice_to_pay).payoff_relevant == 'sure_amount':
                self.in_round(choice_to_pay).payoff = self.participant.vars['icl_sure_payoffs'][choice_to_pay - 1]

            # set payoff as global variable
            # --------------------------------------------------------------------------------------------------------
            self.participant.vars['icl_payoff'] = self.in_round(choice_to_pay).payoff

            # implied switching row
            # --------------------------------------------------------------------------------------------------------
            self.in_round(choice_to_pay).switching_row = self.participant.vars['icl_switching_row']
