import os
import sys
import datetime
import json
import numpy as np
import pandas as pd
import scipy.optimize as opt

# define the path to the folder
file_path = os.path.abspath(__file__)
folder_path = os.path.dirname(file_path)
sys.path.insert(0, folder_path) 

from shared_info import shared_info

class BayesianLR:
    """
    The BayesianLR class is responsible for integrating the Bayesian logistic regression with gamma prior into main.
    """
    
    def __init__(self, 
                 sequence_file = "backend/question_list.json",
                 n_train_iterations = 13,
                 ):
        """
        Initiates the attributes
        """
        # questioning ---------------------------------------------------------------
        self.iteration = 0
        self.n_train_iterations = n_train_iterations
        self.finished = False

        # Load the question list
        with open(sequence_file, 'r') as json_file:
            self.question_list = json.load(json_file)

        # first question
        print(type(self.question_list))
        print(self.question_list["1"])
        self.p_x = self.question_list["1"][0]['p_x'][0]
        self.z = self.question_list["1"][0]['w_p'][0] * (shared_info["x"] - shared_info["y"]) + shared_info["y"]

        # initialization for question dataframe
        starting_data = [[1], [self.p_x], [self.z], [(self.z - shared_info["y"]) / (shared_info["x"] - shared_info["y"])], [None], [None]]
        colnames = ['q_n', 'p_x', 'z', 'w_p', 's', 's_tilde']
        self.train_answers = pd.DataFrame(
            dict(zip(colnames, starting_data))
            ) 
        self.test_answers = pd.DataFrame(columns=colnames)
        
        # draw test sample
        self.draw_test_sample()
        

    def get_train_answers(self):
        return self.train_answers

    def get_test_answers(self):
        return self.test_answers
    
    def get_iteration(self):
        return self.iteration

    def check_finished(self):
        if self.iteration == (self.n_train_iterations + shared_info['number_test_questions'] - 1):
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

    def sequence_next_q(self, answer_vec=None):
        data_next = self.question_list[str(len(answer_vec) + 1)]
        which_answer_seq = np.where([np.all(np.array(sub_dict['s']) == np.array(answer_vec)) for sub_dict in data_next])[0]
        next_q = data_next[int(which_answer_seq[0])]
        print(next_q)

        return next_q['p_x'], next_q['w_p']

    def next_question_train(self, answer):
        """
        Calculates the next values for the lottery after the user's answer
        """

        # asks the question and records the truth
        self.train_answers.loc[self.iteration, "s"] = int(answer)
        self.train_answers.loc[self.iteration, "s_tilde"] = 1 if self.train_answers.loc[self.iteration, "s"] else -1

        # record the current time
        self.train_answers.loc[self.iteration, "timestamp"] = datetime.datetime.now()

        self.iteration += 1
        if self.iteration < self.n_train_iterations:

            # update iteration
            px_value, wp_value = self.sequence_next_q(1 - self.train_answers['s']) # IMPORTANT: 0 IS CHOSE SURE FOR BAYESIAN SEQUENCING
            self.p_x = px_value[-1] if np.array(px_value).size > 1 else px_value
            w_p_t = wp_value[-1] if np.array(wp_value).size > 1 else wp_value
            self.z = w_p_t * (shared_info["x"] - shared_info["y"]) + shared_info["y"]

            self.train_answers.loc[self.iteration, "q_n"] = self.iteration + 1
            self.train_answers.loc[self.iteration, "p_x"] = self.p_x
            self.train_answers.loc[self.iteration, "z"] = self.z
            self.train_answers.loc[self.iteration, "w_p"] = w_p_t

        else:

            self.test_answers.loc[self.test_iteration, "q_n"] = self.test_iteration + 1
            self.p_x = self.test_sample.iloc[self.test_iteration].loc["p_x"]
            self.test_answers.loc[self.test_iteration, "p_x"] = self.p_x
            w_p_t = self.test_sample.iloc[self.test_iteration].loc["w_p"]
            self.z = w_p_t * (shared_info["x"] - shared_info["y"]) + shared_info["y"]
            self.test_answers.loc[self.test_iteration, "z"] = self.z
            self.test_answers.loc[self.test_iteration, "w_p"] = w_p_t

        return self.z, self.p_x

    def next_question_test(self, answer):

        # asks the question and records the truth
        self.test_answers.loc[self.test_iteration, "s"] = int(answer)
        self.test_answers.loc[self.test_iteration, "s_tilde"] = 1 if self.test_answers.loc[self.test_iteration, "s"] else -1

        # record the current time
        self.test_answers.loc[self.test_iteration, "timestamp"] = datetime.datetime.now()

        self.iteration += 1
        self.test_iteration = self.iteration % self.n_train_iterations

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
    
        if self.iteration < self.n_train_iterations:
            return self.next_question_train(answer)
        elif self.iteration < self.n_train_iterations + shared_info['number_test_questions']:
            return self.next_question_test(answer)