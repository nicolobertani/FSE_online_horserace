from otree.api import Page
from .models import Constants

class DecisionPage(Page):
    form_model = 'player'
    form_fields = ['choice']

    def vars_for_template(self):
        return {
            'question': 'Which option do you prefer?'
        }

class Results(Page):
    def vars_for_template(self):
        return {
            'choice': self.player.choice
        }

page_sequence = [DecisionPage, Results]

c