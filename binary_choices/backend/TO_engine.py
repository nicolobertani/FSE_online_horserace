import os
import sys
import datetime
import warnings
import numpy as np
import pandas as pd
import scipy.optimize as opt

# define the path to the folder
file_path = os.path.abspath(__file__)
folder_path = os.path.dirname(file_path)
sys.path.insert(0, folder_path) 

from shared_info import shared_info

class TO:
    """
    The TO class is responsible for integrating trade-off method into main.
    """
    
    def __init__(self, 
                 TO_p_x = 1/3, 
                 TO_r = 15,
                 TO_R = 18,
                 TO_x_0 = 2,
                 TO_x_1 = 8
                 ):
        """
        Initiates the attributes
        """
        # questioning ---------------------------------------------------------------
        self.iteration = 0
        self.TO_x_0_count = 1
        self.last_before_change = False
        self.finished = False

        starting_data = [[self.iteration + 1], [TO_p_x], [TO_r], [TO_R], [TO_x_0], [TO_x_1], [None], [None]]
        colnames = ['q_n', 'p_x', 'r', 'R', 'x_0', 'x_1', 's', 's_tilde']
        self.TO_data = pd.DataFrame(
            dict(zip(colnames, starting_data))
            ) 
        
        # first question
        self.do_TO = True
        self.TO_question_iteration = 0
        self.p_x = self.TO_data.loc[self.iteration, "p_x"]
        self.r = self.TO_data.loc[self.iteration, "r"]
        self.R = self.TO_data.loc[self.iteration, "R"]
        self.x_0 = self.TO_data.loc[self.iteration, "x_0"]
        self.x_1 = self.TO_data.loc[self.iteration, "x_1"]
        

    def get_train_answers(self):
        return self.TO_data

    def get_iteration(self):
        return self.iteration

    def check_finished(self):
        if (self.epsilon <= 0.1) and (self.test_iteration == (shared_info['number_test_questions'] - 1)):
            self.finished = True

    def get_finished(self):
        return self.finished

    def next_question_TO(self, answer):
        """
        Performs trade-off questioning
        """

        # records the answer
        self.TO_data.loc[self.iteration, "s"] = int(answer)
        self.TO_data.loc[self.iteration, "s_tilde"] = 1 if self.TO_data.loc[self.iteration, "s"] else -1

        # record the current time
        self.TO_data.loc[self.iteration, "timestamp"] = datetime.datetime.now()

        # update x_0 if changed preference or after 5 questions
        if self.last_before_change or (self.TO_question_iteration == 5):
            self.TO_question_iteration = 0
            self.last_before_change = False
            self.TO_x_0_count += 1
            
            if answer: # respondent chose the lottery with x_0
                self.x_0 = self.x_1 + .5
            else: # respondent chose the lottery with x_0
                self.x_0 = self.x_1 - .5
            
            self.x_1 = self.x_0 + 2 * self.R - 2 * self.r


        # update outcomes
        if self.TO_question_iteration == 0:
            if answer: # respondent chose the lottery with x_0
                self.x_1 += 1
            else: # respondent chose the lottery with x_0
                self.x_1 -= 1

        else:
            if self.TO_data.loc[self.iteration - 1, "s"] == int(answer): # respondent keeps on preferring the same lottery
                if answer: # respondent chose the lottery with x_0
                    self.x_1 += 1
                else: # respondent chose the lottery with x_0
                    self.x_1 -= 1

            else: # respondent just changed preference to the other same lottery
                self.last_before_change = True
                if self.TO_x_0_count == 3:
                    self.do_TO = False
                    
                if answer: # respondent chose the lottery with x_0
                    self.x_1 += .5
                else: # respondent chose the lottery with x_0
                    self.x_1 -= .5

        self.TO_question_iteration += 1
        self.iteration += 1

        # record the values
        self.TO_data.loc[self.iteration, "q_n"] = self.iteration + 1
        self.TO_data.loc[self.iteration, "p_x"] = self.p_x
        self.TO_data.loc[self.iteration, "r"] = self.r
        self.TO_data.loc[self.iteration, "R"] = self.R
        self.TO_data.loc[self.iteration, "x_0"] = self.x_0
        self.TO_data.loc[self.iteration, "x_1"] = self.x_1
            
        return (self.x_0, self.x_1), self.do_TO
