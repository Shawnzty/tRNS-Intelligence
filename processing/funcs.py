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
from scipy.signal import hilbert
import fathon
from fathon import fathonUtils as fu
from mne.stats import permutation_cluster_test, permutation_cluster_1samp_test



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


def synchrony_R(eeg):
    # Parameters
    n_channels, n_samples = eeg.shape
    # Step 1: Apply Hilbert Transform to get the phase information
    analytical_signal = hilbert(eeg, axis=1)  # Apply along time axis
    phase = np.angle(analytical_signal)  # Instantaneous phase
    # Step 2: Compute Kuramoto Order Parameter r(t) for each time point
    r_t = np.abs(np.sum(np.exp(1j * phase), axis=0)) / n_channels
    # Step 3: Calculate the mean synchrony R over the entire data segment
    R = np.mean(r_t)
    return R


def dfa_alpha(data, min_win=25, max_win=200):
    dfa_data = fu.toAggregated(data)
    pydfa = fathon.DFA(dfa_data)
    wins = fu.linRangeByStep(min_win, max_win)
    n,F = pydfa.computeFlucVec(wins, revSeg=True, polOrd=3)
    H, H_intercept = pydfa.fitFlucVec()
    return H


def remove_outliers(array, low_k, high_k, verbose=False):
    # Calculate Q1 and Q3
    Q1 = np.quantile(array, 0.25)
    Q3 = np.quantile(array, 0.75)
    # Compute the IQR
    IQR = Q3 - Q1
    # Define bounds for outliers
    lower_bound = Q1 - low_k * IQR
    upper_bound = Q3 + high_k * IQR
    # Filter out outliers
    filtered_array = array[(array >= lower_bound) & (array <= upper_bound)]
    if verbose:
        # print(f"Original array:\n{array.describe()}\n")
        print(f"removed {len(array) - len(filtered_array)} outliers out of {len(array)}\n")
    return filtered_array


def sign_of_tvalue(condition1, condition2):
    # Step 1: Calculate median of each column for both conditions
    condition1_med = np.median(condition1, axis=0)
    condition2_med = np.median(condition2, axis=0)
    # Step 2: Subtract condition1_med from condition2_med
    subs = condition2_med - condition1_med
    # Step 3: Convert positive values to 1 and negative values to -1
    subs = np.where(subs > 0, 1, -1)
    
    return subs


def perm_test(condition1, condition2, adjacency):
    # T-test
    f_obs, clusters, cluster_p_values, H0 = permutation_cluster_test(
        [condition1, condition2], n_permutations=2000, adjacency=adjacency, tail=0, verbose=False)
    # Find significant clusters
    significant_clusters = np.nonzero(cluster_p_values < 0.05)[0]

    for idx in significant_clusters:
        cluster = clusters[idx][0]
        if cluster.shape[0] > 1:
            print(f"Cluster {idx}, p-value: {cluster_p_values[idx]}")
            print("Electrodes:", cluster)
    
    sign = sign_of_tvalue(condition1, condition2)
    t_obs = np.sqrt(f_obs) * sign
    # t_obs = np.sqrt(f_obs)
    return t_obs
