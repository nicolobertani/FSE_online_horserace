import random
import numpy as np
import pandas as pd
from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
from binary_choices.config import *
from binary_choices.backend.shared_info import *
import binary_choices.backend.bisection_engine as bisection_engine
import binary_choices.backend.FSE_engine as FSE_engine
import binary_choices.backend.Bayesian_engine as Bayesian_engine
import binary_choices.backend.TO_engine as TO_engine


author = 'Nicolò Bertani'

doc = """
This app sets up a binary choice task to compare 
FSE, standard bisection, Bayesian elicitation, and trade-off method plus FSE.
"""


# ******************************************************************************************************************** #
# *** CLASS SUBSESSION
# ******************************************************************************************************************** #
class Subsession(BaseSubsession):

    # initiate list of sure payoffs and implied switching row in first round
    # ------------------------------------------------------------------------------------------------------------
    def creating_session(self):
        
        if self.round_number == 1:

            if Constants.method == 'Bayesian':
                q_df = pd.read_csv('binary_choices/backend/FSE_table.csv')

            for i, p in enumerate(self.get_players()):
                
                if Constants.method == 'FSE':
                    p.participant.vars.update({
                        'player_model' : FSE_engine.FSE(set_z=shared_info["set_z"])
                    })
                elif Constants.method == 'Bayesian':
                    number_of_questions = np.random.choice(q_df['n.questions'], size = 1, p=q_df['share'])[0]
                    p.participant.vars.update({
                        'player_model' : Bayesian_engine.BayesianLR(
                            sequence_file="binary_choices/backend/question_list.json",
                            n_train_iterations=number_of_questions
                    )
                    })
                elif Constants.method == 'bisection':
                    p.participant.vars.update({
                        'player_model' : bisection_engine.Bisection()
                    })
                elif Constants.method == 'TO':
                    p.participant.vars.update({
                        'player_model' : FSE_engine.FSE(set_z=shared_info["set_z"]),
                        'do_TO' : True,
                        'TO_model' : TO_engine.TO()
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
    # TO
    small_amount = models.FloatField()
    large_amount = models.FloatField()
    x_0 = models.FloatField()
    x_1 = models.FloatField()    
    TO_choice = models.StringField()

    # pwf
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

    # Bayesian info
    # num_Bayesian_questions = models.IntegerField()
