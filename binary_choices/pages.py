import random
import datetime
import pandas as pd
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
        'fixed_payment' : f"{experiment_text['amount_currency']}{fixed_payment}",
        'x_str' : f"{experiment_text['amount_currency']}{shared_info['x']}",
        'y_str' : f"{experiment_text['amount_currency']}{shared_info['y']}",
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
        # self.player.num_Bayesian_questions = int(self.player.participant.vars['player_model'].n_train_iterations)
        
        vars = vars_for_all_templates(self)

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
            'x_prob': f"{shared_info['practice_p'] * 100:.2f}".rstrip('0').rstrip('.') + "%",
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
            'comp_q1_text' : experiment_text["comp_q1"].format(practice_lottery_text.rstrip('.').replace('\n', ' ')),
            'comp_q1_opt1' : f"{experiment_text['amount_currency']}{shared_info['practice_z']}".rjust(5),
            'comp_q1_opt2' : f"{experiment_text['amount_currency']}{shared_info['x']}".rjust(5),
            'comp_q1_opt3' : f"{experiment_text['amount_currency']}{shared_info['y']}".rjust(5),
            'comp_q2_text' : experiment_text["comp_q2"].format(practice_sure_text.rstrip('.').replace('\n', ' ')),
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
# *** PAGE TO DECISION *** #
# ******************************************************************************************************************** #
class TO_Decision(Page):

    def is_displayed(self):
        return self.player.participant.vars['do_TO'] == True

    # form model and form fields
    # ----------------------------------------------------------------------------------------------------------------
    form_model = 'player'
    form_fields = ['TO_choice']    

    # variables for template
    # ----------------------------------------------------------------------------------------------------------------
    def vars_for_template(self):

        self.player.q_timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.player.p_x = float(self.player.participant.vars['TO_model'].p_x)
        self.player.small_amount = float(self.player.participant.vars['TO_model'].r)
        self.player.large_amount = float(self.player.participant.vars['TO_model'].R)
        
        if self.subsession.round_number == 1:
            self.player.x_0 = float(self.player.participant.vars['TO_model'].x_0)
            self.player.x_1 = float(self.player.participant.vars['TO_model'].x_1)
        else:
            previous_choice = self.player.in_round(self.subsession.round_number - 1).TO_choice == 'lottery_R'
            (x_0, x_1), self.player.participant.vars['do_TO'] = self.player.participant.vars['TO_model'].next_question(previous_choice)
            self.player.x_0 = float(x_0)
            self.player.x_1 = float(x_1)

        vars = vars_for_all_templates(self)
        vars.update({
            'page': self.subsession.round_number,
            'x_prob': f"{self.player.p_x * 100:.2f}".rstrip('0').rstrip('.') + "%",
            'y_prob' : f"{(1 - self.player.p_x) * 100:.2f}".rstrip('0').rstrip('.') + "%",
            'r' : f"{experiment_text['amount_currency']}{self.player.small_amount:.2f}".rstrip('0').rstrip('.'),
            'R' : f"{experiment_text['amount_currency']}{self.player.large_amount:.2f}".rstrip('0').rstrip('.'),
            'x_0': f"{experiment_text['amount_currency']}{self.player.x_0:.2f}".rstrip('0').rstrip('.'),
            'x_1': f"{experiment_text['amount_currency']}{self.player.x_1:.2f}".rstrip('0').rstrip('.'),
            'lottery_first' : random.choice([True, False]),
            'large_opt_first' : self.player.participant.vars['large_opt_first'],
        })
        return vars


# ******************************************************************************************************************** #
# *** PAGE DECISION *** #
# ******************************************************************************************************************** #
class Decision(Page):

    def is_displayed(self):
        return (self.player.participant.vars['do_TO'] == False) and (self.player.participant.vars['last_q'] == False)

    # form model and form fields
    # ----------------------------------------------------------------------------------------------------------------
    form_model = 'player'
    form_fields = ['choice']    

    # variables for template
    # ----------------------------------------------------------------------------------------------------------------
    def vars_for_template(self):

        self.player.q_timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        if Constants.method == 'TO':
            
            if self.subsession.round_number == (self.player.participant.vars['TO_model'].get_iteration() + 1):
                
                # save the last choice of the TO part
                previous_choice = self.player.in_round(self.subsession.round_number - 1).TO_choice == 'lottery_R'
                self.player.participant.vars['TO_model'].next_question(previous_choice)
                # fit and store the utility transformation
                TO_sequence, u_par = self.player.participant.vars['TO_model'].fit_utility()
                self.player.participant.vars['player_model'].incorporate_utility_transformation(TO_sequence, u_par)

                # set the first question of the pwf part
                self.player.z = float(self.player.participant.vars['player_model'].z)
                self.player.p_x = float(self.player.participant.vars['player_model'].p_x)
            
            else:
                previous_choice = self.player.in_round(self.subsession.round_number - 1).choice == 'sure_amount'
                (z, p_x), self.player.participant.vars['last_q'] = self.player.participant.vars['player_model'].next_question(previous_choice)
                self.player.z = float(z)
                self.player.p_x = float(p_x)

            page_number = int(self.player.participant.vars['TO_model'].get_iteration() + self.player.participant.vars['player_model'].get_iteration() + 2)

        else:
            if self.subsession.round_number == 1:
                self.player.z = float(self.player.participant.vars['player_model'].z)
                self.player.p_x = float(self.player.participant.vars['player_model'].p_x)

            else:
                previous_choice = self.player.in_round(self.subsession.round_number - 1).choice == 'sure_amount'
                (z, p_x), self.player.participant.vars['last_q'] = self.player.participant.vars['player_model'].next_question(previous_choice)
                self.player.z = float(z)
                self.player.p_x = float(p_x)

            page_number = self.subsession.round_number 

        vars = vars_for_all_templates(self)
        vars.update({
            'page': page_number,
            'x_prob': f"{self.player.p_x * 100:.2f}".rstrip('0').rstrip('.') + "%",
            'y_prob' : f"{(1 - self.player.p_x) * 100:.2f}".rstrip('0').rstrip('.') + "%",
            'z_str': f"{experiment_text['amount_currency']}{self.player.z:.2f}".rstrip('0').rstrip('.'),
            'lottery_first' : random.choice([True, False]),
            'large_opt_first' : self.player.participant.vars['large_opt_first'],
        })
        return vars


# ******************************************************************************************************************** #
# *** PAGE RESULTS *** #
# ******************************************************************************************************************** #
class Results(Page):

    # skip results until last page
    # ----------------------------------------------------------------------------------------------------------------
    def is_displayed(self):
        return self.player.participant.vars['last_q'] == True

    # variables for template
    # ----------------------------------------------------------------------------------------------------------------
    def vars_for_template(self):

        self.player.end_timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        vars = vars_for_all_templates(self)
        vars.update({
            'real_incentives' : real_incentives,
            'is_winner' : self.player.participant.vars['winning_participant'],
        })
        self.player.winning_participant = self.player.participant.vars['winning_participant']

        if self.player.participant.vars['winning_participant']:

            # only select from pwf rounds
            if Constants.method == 'TO':
                self.player.random_draw = random.randrange(len(self.player.in_all_rounds()) - self.player.participant.vars['player_model'].get_iteration(), len(self.player.in_all_rounds()))
            else:
                self.player.random_draw = random.randrange(len(self.player.in_all_rounds()))
            
            self.player.winning_choice = self.player.random_draw + 1
            
            winning_s = self.player.in_round(self.player.random_draw + 1).choice == 'sure_amount'
            winning_p_x = self.player.in_round(self.player.random_draw + 1).p_x
            winning_z = self.player.in_round(self.player.random_draw + 1).z
            simulated_lottery_outcome = random.random() < winning_p_x
            
            if winning_s == 1:
                extra_payoff = f"{experiment_text['amount_currency']}{winning_z:.2f}".rstrip('0').rstrip('.')
            else:
                if simulated_lottery_outcome:
                    extra_payoff = f"{experiment_text['amount_currency']}{shared_info['x']:.2f}".rstrip('0').rstrip('.')
                else:
                    extra_payoff = f"{experiment_text['amount_currency']}{shared_info['y']:.2f}".rstrip('0').rstrip('.')
            
            self.player.extra_payoff = extra_payoff
                
            vars.update({
                'winning_s' : winning_s,
                'x_prob': f"{winning_p_x * 100:.2f}".rstrip('0').rstrip('.') + "%",
                'y_prob' : f"{(1 - winning_p_x) * 100:.2f}".rstrip('0').rstrip('.') + "%",
                'z_str': f"{winning_z:.2f}".rstrip('0').rstrip('.'),
                'extra_payoff' : extra_payoff,
            })

        else:
            
            vars.update({
                'winning_s' : False,
                'x_prob': False,
                'y_prob' : False,
                'z_str': False,
                'extra_payoff' : False,
            })

        return vars


# ******************************************************************************************************************** #
# *** PAGE SEQUENCE *** #
# ******************************************************************************************************************** #
page_sequence = [Practice, ComprehensionQuestion, ExpIntro, TO_Decision, Decision]
# page_sequence = [TO_Decision, Decision]

if Constants.instructions:
    page_sequence.insert(0, Instructions)

if Constants.results:
    page_sequence.append(Results)
