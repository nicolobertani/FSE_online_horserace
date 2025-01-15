import random
import datetime
from otree.api import Currency as c, currency_range
from . import models
from ._builtin import Page, WaitPage
from .models import Constants
from .backend.shared_info import *


# variables for all templates
# --------------------------------------------------------------------------------------------------------------------
def vars_for_all_templates(self):
    out = shared_info.copy()
    out.update(experiment_text)
    out.update(
    {
        'p_hi': "{0:.0f}".format(Constants.probability) + "%",
        'p_lo': "{0:.0f}".format(100 - Constants.probability) + "%",
        'hi':   c(Constants.lottery_hi),
        'lo':   c(Constants.lottery_lo)
    })
    return out


# ******************************************************************************************************************** #
# *** CLASS INSTRUCTIONS *** #
# ******************************************************************************************************************** #
class Instructions(Page):

    # only display instruction in round 1
    # ----------------------------------------------------------------------------------------------------------------
    def is_displayed(self):
        return self.subsession.round_number == 1

    def vars_for_template(self):
        
        self.player.instruction_timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        vars = vars_for_all_templates(self)
        vars.update({
            'n': Constants.num_choices
        })
        return vars


# ******************************************************************************************************************** #
# *** PAGE PRACTICE *** #
# ******************************************************************************************************************** #
class Practice(Page):

    def is_displayed(self):
        return self.subsession.round_number == 1

    # form model and form fields
    # ----------------------------------------------------------------------------------------------------------------
    form_model = 'player'
    form_fields = ['practice_choice']

    # variables for template
    # ----------------------------------------------------------------------------------------------------------------
    def vars_for_template(self):

        self.player.practice_timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        vars = vars_for_all_templates(self)
        vars.update({
            'x_str': f"{experiment_text['amount_currency']}{shared_info['x']}",
            'x_prob': f"{shared_info['practice_p'] * 100:.2f}".rstrip('0').rstrip('.') + "%",
            'y_str' : f"{experiment_text['amount_currency']}{shared_info['y']}",
            'y_prob' : f"{(1 - shared_info['practice_p']) * 100:.2f}".rstrip('0').rstrip('.') + "%",
            'z_str': f"{experiment_text['amount_currency']}{shared_info["practice_z"]:.2f}".rstrip('0').rstrip('.')
        })
        return vars


# ******************************************************************************************************************** #
# *** PAGE COMPREHENSION QUESTION *** #
# ******************************************************************************************************************** #
class ComprehensionQuestion(Page):

    def is_displayed(self):
        return self.subsession.round_number == 1

    # form model and form fields
    # ----------------------------------------------------------------------------------------------------------------
    form_model = 'player'
    form_fields = ['comp_q1', 'comp_q2']

    # variables for template
    # ----------------------------------------------------------------------------------------------------------------
    def vars_for_template(self):
        
        self.player.comp_timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        practice_lottery_text = experiment_text["sentence_lottery"].format(
            f"{experiment_text['amount_currency']}{shared_info['x']}",
            f"{shared_info['practice_p'] * 100:.2f}".rstrip('0').rstrip('.') + "%",
            f"{experiment_text['amount_currency']}{shared_info['y']}",
            f"{(1 - shared_info['practice_p']) * 100:.2f}".rstrip('0').rstrip('.') + "%",
        )

        practice_sure_text = experiment_text["sentence_sure"].format(
            f"{experiment_text['amount_currency']}{shared_info["practice_z"]:.2f}".rstrip('0').rstrip('.')
        )

        vars = vars_for_all_templates(self)
        vars.update({
            'comp_q1_text': experiment_text["comp_q1"].format(practice_lottery_text.rstrip('.').replace('\n', ' ')),
            'comp_q1_opt1' : f"{experiment_text['amount_currency']}{shared_info['practice_z']}".rjust(5),
            'comp_q1_opt2' : f"{experiment_text['amount_currency']}{shared_info['x']}".rjust(5),
            'comp_q1_opt3' : f"{experiment_text['amount_currency']}{shared_info['y']}".rjust(5),
            'comp_q2_text': experiment_text["comp_q2"].format(practice_sure_text.rstrip('.').replace('\n', ' ')),
            'comp_q2_opt1' : f"{experiment_text['amount_currency']}{shared_info['practice_z']}".rjust(5),
            'comp_q2_opt2' : f"{experiment_text['amount_currency']}{shared_info['x']}".rjust(5),
            'comp_q2_opt3' : f"{experiment_text['amount_currency']}{shared_info['y']}".rjust(5),
        })

        return vars

class ExpIntro(Page):

    # only display instruction in round 1
    # ----------------------------------------------------------------------------------------------------------------
    def is_displayed(self):
        return self.subsession.round_number == 1

    def vars_for_template(self):

        self.player.intro_timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        return vars_for_all_templates(self)



# ******************************************************************************************************************** #
# *** PAGE DECISION *** #
# ******************************************************************************************************************** #
class Decision(Page):

    # form model and form fields
    # ----------------------------------------------------------------------------------------------------------------
    form_model = 'player'
    form_fields = ['choice']

    # variables for template
    # ----------------------------------------------------------------------------------------------------------------
    def vars_for_template(self):

        self.player.q_timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # specify info for progress bar
        total = Constants.num_choices
        page = self.subsession.round_number
        progress = page / total * 100

        vars = vars_for_all_templates(self)
        vars.update({
            'page':        page,
            'total':       total,
            'progress':    progress,
            'sure_payoff': self.participant.vars['icl_sure_payoffs'][page - 1],
            'large_opt_first' : random.choice([True, False]),
            'lottery_first' : random.choice([True, False]),

        })
        return vars

    # set sure payoffs for next choice, payoffs, and switching row
    # ----------------------------------------------------------------------------------------------------------------
    def before_next_page(self):
        self.player.set_sure_payoffs()
        self.player.update_switching_row()
        self.player.set_payoffs()


# ******************************************************************************************************************** #
# *** PAGE RESULTS *** #
# ******************************************************************************************************************** #
class Results(Page):

    # skip results until last page
    # ----------------------------------------------------------------------------------------------------------------
    def is_displayed(self):
        return self.subsession.round_number == Constants.num_rounds

    # variables for template
    # ----------------------------------------------------------------------------------------------------------------
    def vars_for_template(self):

        self.player.end_timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # payoff information
        choice_to_pay = self.participant.vars['icl_choice_to_pay']
        option_to_pay = self.player.in_round(choice_to_pay).choice
        payoff_relevant = self.player.in_round(choice_to_pay).payoff_relevant
        sure_payoff = self.player.participant.vars['icl_sure_payoffs'][choice_to_pay - 1]

        vars = vars_for_all_templates(self)
        vars.update({
            'sure_payoff':     sure_payoff,
            'option_to_pay':   option_to_pay,
            'payoff_relevant': payoff_relevant,
            'payoff':          self.player.in_round(choice_to_pay).payoff,
        })
        return vars


# ******************************************************************************************************************** #
# *** PAGE SEQUENCE *** #
# ******************************************************************************************************************** #
page_sequence = [Practice, ComprehensionQuestion, ExpIntro, Decision]

if Constants.instructions:
    page_sequence.insert(0, Instructions)

if Constants.results:
    page_sequence.append(Results)
