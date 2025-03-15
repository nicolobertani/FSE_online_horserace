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
        self.finished = False

        starting_data = [[self.iteration + 1], [TO_p_x], [TO_r], [TO_R], [TO_x_0], [TO_x_1], [None], [None]]
        colnames = ['q_n', 'p_x', 'r', 'R', 'x_0', 'x_1', 's', 's_tilde']
        self.TO_data = pd.DataFrame(
            dict(zip(colnames, starting_data))
            ) 
        self.test_answers = pd.DataFrame(columns=colnames)
        
        # first question
        self.do_TO = True
        self.TO_question_iteration = 0
        self.p_x = self.TO_data.loc[self.iteration, "p_x"]
        self.r = self.TO_data.loc[self.iteration, "r"]
        self.R = self.TO_data.loc[self.iteration, "R"]
        self.x_0 = self.TO_data.loc[self.iteration, "x_0"]
        self.x_1 = self.TO_data.loc[self.iteration, "x_1"]
        
        # draw test sample
        self.draw_test_sample()
        

    def get_closest_z(self, z):
        """
        Returns the closest bisection point in the set z
        """
        distances = np.abs(np.array(self.set_z) - z)
        closest_indices = np.where(distances == np.min(distances))[0]
        closest_z_values = np.array(self.set_z)[closest_indices]
        
        if len(closest_z_values) > 1:
            closest_z = np.random.choice(closest_z_values)
        else:
            closest_z = closest_z_values[0]
        
        return closest_z

    def getEpsilon(self):
        return self.epsilon

    def get_train_answers(self):
        return self.train_answers

    def get_test_answers(self):
        return self.test_answers
    
    def get_iteration(self):
        return self.iteration

    def check_finished(self):
        if (self.epsilon <= 0.1) and (self.test_iteration == (shared_info['number_test_questions'] - 1)):
            self.finished = True

    def get_finished(self):
        return self.finished

    def draw_test_sample(self):
        self.test_iteration = 0

        row_indices = np.arange(shared_info["holdout_questions"].shape[0])
        test_indices = np.random.choice(row_indices, shared_info['number_test_questions'], replace=False)
        self.test_sample = shared_info["holdout_questions"].iloc[test_indices]
        self.test_sample = pd.concat(
            [self.test_sample,
             pd.DataFrame([{'p_x': np.nan, 'w_p': np.nan}])], 
             ignore_index=True)

    def next_question_TO(self, answer):
        """
        Performs trade-off questioning
        """

        if self.do_TO:
            
            # records the answer
            self.TO_data.loc[self.iteration, "s"] = int(answer)
            self.TO_data.loc[self.iteration, "s_tilde"] = 1 if self.TO_data.loc[self.iteration, "s"] else -1

            # record the current time
            self.TO_data.loc[self.iteration, "timestamp"] = datetime.datetime.now()

            # update outcomes
            if self.TO_data.loc[self.iteration - 1, "s"] == answer: # respondent keeps on preferring the same lottery
                if answer: # respondent chose the lottery with x_0
                    self.x_1 += 1
                else: # respondent chose the lottery with x_0
                    self.x_1 -= 1
            else: # respondent just changed preference to the other same lottery
                self.just_changed = True
                self.TO_question_iteration = 0
                if answer: # respondent chose the lottery with x_0
                    self.x_1 += .5
                else: # respondent chose the lottery with x_0
                    self.x_1 -= .5

            self.TO_question_iteration += 1
            self.iteration += 1

            
        else:

            # initialization for question dataframe
            starting_p_x = .9
            starting_z = (shared_info["x"] + shared_info["y"]) / 2
            starting_data = [[self.iteration + 1], [starting_p_x], [starting_z], [(starting_z - shared_info["y"]) / (shared_info["x"] - shared_info["y"])], [None], [None]]
            colnames = ['q_n', 'p_x', 'z', 'w_p', 's', 's_tilde']
            self.train_answers = pd.DataFrame(
                dict(zip(colnames, starting_data))
                ) 
            self.test_answers = pd.DataFrame(columns=colnames)
            
            # first question
            self.z = self.train_answers.loc[self.iteration, "z"]
            self.p_x = self.train_answers.loc[self.iteration, "p_x"]

            # initialization for LPs
            self.epsilon = np.inf
            self.A1 = np.zeros((FSE.M, FSE.M))
            np.fill_diagonal(self.A1, -1)

            self.lower_bound = I_spline(x=self.set_p, k=FSE.ORDER, interior_knots=FSE.CHOSEN_XI, individual=True)[FSE.M-1]
            self.upper_bound = I_spline(x=self.set_p, k=FSE.ORDER, interior_knots=FSE.CHOSEN_XI, individual=True)[0]
            self.D = self.upper_bound - self.lower_bound


    def next_question_train(self, answer):
        """
        Calculates the next values for the lottery after the user's answer
        """
        # records the answer
        self.train_answers.loc[self.iteration, "s"] = int(answer)
        self.train_answers.loc[self.iteration, "s_tilde"] = 1 if self.train_answers.loc[self.iteration, "s"] else -1

        # record the current time
        self.train_answers.loc[self.iteration, "timestamp"] = datetime.datetime.now()

        # prepare parameters for LPs
        A2 = self.train_answers["s_tilde"].values * I_spline(x = self.train_answers["p_x"], k=FSE.ORDER, interior_knots=FSE.CHOSEN_XI, individual=True) # question part
        A = np.column_stack((self.A1, A2)).T
        b = np.concatenate((np.zeros(FSE.M), self.train_answers["s_tilde"].values * self.train_answers["w_p"].values))

        # update bounds
        for i, local_x in enumerate(self.set_p):

            c = np.array(
                I_spline(x = local_x, k = 3, interior_knots = FSE.CHOSEN_XI, individual = True)
            )

            min_problem = opt.linprog(
                c = c,
                A_ub = A,
                b_ub = b,
                A_eq = np.array([np.array([1] * FSE.M)]),
                b_eq = np.array([1])
            )
            self.lower_bound[i] = np.dot(min_problem.x, c)

            max_problem = opt.linprog(
                c = -c, # for maximization
                A_ub = A,
                b_ub = b,
                A_eq = np.array([np.array([1] * FSE.M)]),
                b_eq = np.array([1])
            )
            self.upper_bound[i] = np.dot(max_problem.x, c)

        # calculate max difference based on updated bounds
        self.D = np.round(self.upper_bound - self.lower_bound, 6)
        self.epsilon = np.max(self.D)

        self.iteration += 1
        if self.epsilon > .1:

            # update iteration
            self.train_answers.loc[self.iteration, "q_n"] = self.iteration + 1

            # find next p
            candidates = self.D == np.max(self.D)
            if np.sum(candidates) == 1:  # if one point exists
                self.train_answers.loc[self.iteration, "p_x"] = self.set_p[candidates]
            else:  # if multiple points exist
                warnings.warn('Warning: multiple optimal bisection points')
                abs_distance_from_middle = np.abs(self.set_p[candidates] - 0.5)
                self.train_answers.loc[self.iteration, "p_x"] = np.array(self.set_p[candidates])[abs_distance_from_middle == np.max(abs_distance_from_middle)][0]

            # compute next z and w.p
            w_p_t = (self.upper_bound + self.lower_bound)[self.set_p == self.train_answers.loc[self.iteration, "p_x"]] / 2 # p_w wiing lottery
            candidate_z_t = w_p_t * (shared_info["x"] - shared_info["y"]) + shared_info["y"] # z is sure amount
            if (self.set_z is None):
                self.train_answers.loc[self.iteration, "z"] = candidate_z_t
                self.train_answers.loc[self.iteration, "w_p"] = w_p_t
            else:
                self.train_answers.loc[self.iteration, "z"] = self.get_closest_z(candidate_z_t)
                self.train_answers.loc[self.iteration, "w_p"] = (self.train_answers.loc[self.iteration, "z"] - shared_info["y"]) / (shared_info["x"] - shared_info["y"])

            # saves z and p_w
            self.z = self.train_answers.loc[self.iteration, "z"]
            self.p_x = self.train_answers.loc[self.iteration, "p_x"]

        else:
            
            self.test_answers.loc[self.test_iteration, "q_n"] = self.test_iteration + 1
            self.p_x = self.test_sample.iloc[self.test_iteration].loc["p_x"]
            self.test_answers.loc[self.test_iteration, "p_x"] = self.p_x
            w_p_t = self.test_sample.iloc[self.test_iteration].loc["w_p"]
            self.z = w_p_t * (shared_info["x"] - shared_info["y"]) + shared_info["y"]
            self.test_answers.loc[self.test_iteration, "z"] = self.z
            self.test_answers.loc[self.test_iteration, "w_p"] = w_p_t

        return self.z, self.p_x

    def next_question(self, answer):
        self.check_finished()

        if self.getEpsilon() > 0.1:
            return self.next_question_train(answer)
        elif self.test_iteration < shared_info['number_test_questions']:
            return self.next_question_test(answer)
    