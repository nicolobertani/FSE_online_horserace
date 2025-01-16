import random
from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
from binary_choices.config import *
from binary_choices.backend.shared_info import *
import binary_choices.backend.bisection_engine as bisection_engine
import binary_choices.backend.FSE_engine as FSE_engine
import binary_choices.backend.Bayesian_engine as Bayesian_engine


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
                if i % 2 == 0:
                    p.participant.vars.update({
                        'player_model' : bisection_engine.Bisection(),
                    })
                else:
                    p.participant.vars.update({
                        'player_model' : FSE_engine.FSE(set_z=shared_info["set_z"]),
                    })

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
    extra_payoff = models.StringField()
    random_draw = models.IntegerField()
