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

relative_path = os.path.join('..', '..', '..', 'data')

def load_info():
    info_path = os.path.join(relative_path, 'tRNS experiment.csv')
    exp_info = pd.read_csv(info_path)
    return exp_info

def load_rpm_answers():
    rpm_path = os.path.join('..', '..', 'exp_program', 'ravens_info.csv')
    rpm_answers = pd.read_csv(rpm_path)
    return rpm_answers

