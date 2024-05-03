import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from scipy import stats
from scipy.stats import lognorm, exponnorm, invgauss
from scipy.optimize import curve_fit
from sklearn.metrics import mean_squared_error
from scipy.stats import ttest_ind, ttest_rel, mannwhitneyu
from pyddm import Model, Sample, Fittable, Fitted
from pyddm.models import DriftConstant, NoiseConstant, BoundConstant, OverlayNonDecision, ICPointSourceCenter, LossRobustLikelihood
from pyddm.functions import fit_adjust_model, display_model
import pyddm.plot


def load_info():
    info_path = os.path.join('..', '..', '..', 'data', 'tRNS experiment.csv')
    exp_info = pd.read_csv(info_path)
    return exp_info


def load_rpm_answers():
    rpm_path = os.path.join('..', '..', 'exp_program', 'ravens_info.csv')
    rpm_answers = pd.read_csv(rpm_path)
    return rpm_answers


def load_subjects_behavior():
    exp_info = load_info()
    rpm_answers = load_rpm_answers()
    task_times = ['pre', 'post']
    subjects_behavior = pd.DataFrame(columns=['subject id', 'condition', 'report', 'task time', 'question', 'level', 'subject answer', 'correct answer', 'answered', 'correct', 'reaction time'])
    for subject_id in range (1, 27):
        for i,task_time in enumerate(task_times):
            filename = f'../../../data/{subject_id}/{subject_id}_{i+1}.csv'
            one_behavior = pd.read_csv(filename)
            one_behavior.rename(columns={'answer': 'subject answer'}, inplace=True)

            # Add subject_id and task_time to one_behavior DataFrame
            one_behavior['subject id'] = subject_id
            one_behavior['task time'] = task_times[i]  
            # Reorder columns to match subjects_behavior DataFrame
            one_behavior = one_behavior[['subject id', 'question', 'subject answer', 'reaction time', 'task time']]
            # Append one_behavior data to subjects_behavior DataFrame
            subjects_behavior = pd.concat([subjects_behavior, one_behavior], ignore_index=True)

    for row in range(len(subjects_behavior)):
        subject_id = subjects_behavior.loc[row, 'subject id']

        condition = exp_info.loc[exp_info['subject id'] == subject_id, 'Condition'].values[0]
        report = exp_info.loc[exp_info['subject id'] == subject_id, 'Report'].values[0]
        subjects_behavior.at[row, 'condition'] = condition
        subjects_behavior.at[row, 'report'] = report

        question = subjects_behavior.loc[row, 'question']
        level = rpm_answers.loc[rpm_answers['question'] == question, 'level'].values[0]
        correct_answer = rpm_answers.loc[rpm_answers['question'] == question, 'answer'].values[0]
        subjects_behavior.at[row, 'level'] = level
        subjects_behavior.at[row, 'correct answer'] = correct_answer

        # Fill in 'answered' and 'correct' columns
        subjects_behavior.at[row, 'answered']  = 1 if subjects_behavior.loc[row, 'subject answer'] != 0 else 0
        subjects_behavior.at[row, 'correct'] = 1 if subjects_behavior.loc[row, 'subject answer'] == subjects_behavior.loc[row, 'correct answer'] else 0
        # if subjects_behavior.loc[row, 'subject answer'] != 0:
        #     subjects_behavior.at[row, 'answered'] = 1 # 1 means the subject answered the question
        #     if subjects_behavior.loc[row, 'subject answer'] == subjects_behavior.loc[row, 'correct answer']:
        #         subjects_behavior.at[row, 'correct'] = 1 # 1 means the subject answered the question and got it right
        #     else:
        #         subjects_behavior.at[row, 'correct'] = 0 # 0 means the subject answered the question but got it wrong
        # else:
        #     subjects_behavior.at[row, 'answered'] = 0 # 0 means the subject did not answer the question
        #     subjects_behavior.at[row, 'correct'] = -1 # -1 means the subject did not answer the question
        
    return subjects_behavior

