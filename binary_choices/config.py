# <imports>
from otree.api import Currency as c
from otree.constants import BaseConstants
from .backend.shared_info import *

# ******************************************************************************************************************** #
# *** CLASS CONSTANTS *** #
# ******************************************************************************************************************** #
class Constants(BaseConstants):

    name_in_url = 'binary_choices'
    players_per_group = None
    num_rounds = 50
    # num_rounds = max([31 + 15, len(shared_info['set_p_bisection']) * shared_info["number_bisection_steps"] + shared_info['number_test_questions'] + 1])
    buttons = False
    progress_bar = False

    # ---------------------------------------------------------------------------------------------------------------- #
    # --- Customizable variables --- #
    # ---------------------------------------------------------------------------------------------------------------- #

    # uncomment the elicitation method that you wish to use
    method = 'FSE'
    # method = 'bisection'
    # method = 'Bayesian'
    # method = 'TO'

    # show instructions at the beginning of the experiment
    instructions = True

    # show results of the random incentive scheme at the end of the experiment
    results = True

    # this is where you can specify the Prolific completion link
    completionlink = ''
