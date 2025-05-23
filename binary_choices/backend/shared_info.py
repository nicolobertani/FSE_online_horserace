import numpy as np
import pandas as pd

real_incentives = True

shared_info = {
    "x" : 18,
    'y' : 2,
    "step_p" : 0.1,
    "step_z" : 0.5,
    "practice_p" : 0.6,
    "practice_z" : 5,
    "holdout_questions" : pd.DataFrame({
        "p_x" : [.01, .05, .10, .25, .4, .5, .6, .75, .9, .95, .99],
        "w_p" : [.01, .05, .10, .25, .4, .5, .6, .75, .9, .95, .99]
    }),
    "number_test_questions" : 5, # 2 or less becomes problematic for the code
}

shared_info.update({
    'set_p' : np.arange(0, 1, shared_info["step_p"])[1:],
    'set_z' : np.arange(shared_info['y'], shared_info["x"], shared_info["step_z"])[1:]
})

shared_info.update({
    'set_p_bisection' : np.arange(0, 1, 1/6)[1:],
    'number_bisection_steps' : 5,
})

currency = "$"
fixed_payment = "2"
share_winners = 1/30

# Condiational instructions
if real_incentives:
    payment_info = f"""
        For participating in this experiment, you will receive a fixed payment of {currency}{fixed_payment}.
        Additionally, you have a chance to be selected to win a bonus payment of up to {currency}{shared_info['x']}, depending on your choices.
        If you are selected, one of your choices from the experiment will be randomly picked, and the associated reward will be added to your payment.
        If the chosen reward is a lottery, the bonus payment will be determined by simulating the outcome of that lottery.
        """
    instructions_reminder = ["""
    The previous question was just for practice.
    The experiment will now start.
    """,
    "All choices you will make from now could be selected to be added to your final payment."
    ]
else: 
    payment_info = f"For participating in this experiment, you will receive a fixed payment of {currency}{fixed_payment}."
    instructions_reminder = ["""
    The previous question was just for practice.
    The experiment will now start.
    """]

# Set question text
experiment_text = {
    "welcome" : "Welcome to the experiment!",

    "instructions" : [
        """
        You will be presented with a series of questions.
        In each question, you will choose between receiving a fixed amount of money or participating in a lottery.
        To make your choice, simply select the option you prefer on the screen and then confirm your choice.
        """,
        """
        Please take the time to carefully read each option before making your choice. 
        In each option, the information that can vary between choices is highlighted in bold.
        """,
        "There are no right or wrong answers: we are only interested in your preferences.",
        # f"""
        # For participating in this experiment, you will receive a fixed payment of {currency}{fixed_payment}.
        # Additionally, you have a chance to win a bonus payment of up to {currency}{shared_info['x']}, depending on your choices.
        # One in {int(1/share_winners)} participants will be randomly selected for the bonus payment.
        # If you are selected, one of your choices from the experiment will be randomly picked, and the associated reward will be added to your payment.
        # If the chosen reward is a lottery, the bonus payment will be determined by simulating the outcome of that lottery.
        # """,
        payment_info,
        "You will now be presented with a practice question to help you become familiar with the task, followed by two comprehension questions.",
        "Press the button below to proceed to the practice question."
    ],
    
    "instructions_reminder" : instructions_reminder, # type: ignore
    
    "comp_instructions" : "Please read the instructions carefully and answer the question below.",

    "comp_q1" : 'Suppose that, in the previous question, you had opted for "{}".\nWhat is the maximal amount you could win?',
    
    "comp_q2" : 'Now suppose instead that, in the previous question, you had opted for "{}".\nWhat is the maximal amount you could win in this case?',

    "amount_currency" : currency,
    
    "question_header" : "Which of the following options do you prefer?",
    
    "sentence_sure" : "Receiving {} for sure.",
    # "sentence_lottery" : "A lottery where you can either receive {} with {} probability, or receive {} otherwise.",
    # "sentence_lottery" : "A lottery that will pay:\n\n{} with {} probability,\nor\n{} with {} probability.",
    
    "sentence_lottery" : "A lottery where you can either receive:\n\n{} with {} probability\nor\n{} with {} probability.",
    
    "confirm" : "I confirm my choice.",
    
    "final_message" : "The experiment is over, thank you for your help!"
}
