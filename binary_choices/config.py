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
    num_rounds = max([31, len(shared_info['set_p_bisection']) * shared_info["number_bisection_steps"] + shared_info['number_test_questions'] + 1])

    # ---------------------------------------------------------------------------------------------------------------- #
    # --- Overall Settings and Appearance --- #
    # ---------------------------------------------------------------------------------------------------------------- #

    # render buttons instead of radio buttons
    # if <buttons = True>, a button will be displayed for each choice ("A", "B", "Indifferent") instead of radio buttons
    # that is, subjects only click a single button than rather choosing a radio button and clicking on "Next"
    # <buttons = True> accelerates input of choices but implies that decisions can not be modified
    buttons = False

    # show progress bar
    # if <progress_bar = True> and <one_choice_per_page = True>, a progress bar is rendered
    # if <progress_bar = False>, no information with respect to the advance within the task is displayed
    # the progress bar graphically depicts the advance within the task in terms of how many decision have been made
    # further, information in terms of "page x out of <num_choices>" (with x denoting the current choice) is provided
    progress_bar = False

    # show instructions page
    # if <instructions = True>, a separate template "Instructions.html" is rendered prior to the task
    # if <instructions = False>, the task starts immediately (e.g. in case of printed instructions)
    instructions = True

    # show results page summarizing the task's outcome including payoff information
    # if <results = True>, a separate page containing all relevant information is displayed after finishing the task
    # if <results = False>, the template "Decision.html" will not be rendered
    results = True
    completionlink = 'https://app.prolific.com/submissions/complete?cc=C1ML7VWD'


