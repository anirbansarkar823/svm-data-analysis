""" file: ./scoring.py
Script for scoring an asset. The inputs will be provided through
command line arguments. The list of arguments are given below;
    * -df path_to_cleaned_csv_file
    * -s separator_used
    * -yml path_to_yaml_file

The data columns are categorised as follows:
    1. whose scoring is done using single threshold.
    2. whose scoring is done using two threshold.
    3. multi-choice multi-select.
    4. multi-choice single-select.
"""

import pandas as pd
import numpy as np


from collections import deque, OrderedDict

from cleaning_pipeline import FR_T_TIME, FR_T_STR_NR, FR_T_NUM, FR_T_MULT_SEL


def str_to_num(numstr):
    try:
        return int(numstr)
    except ValueError:
        try:
            return float(numstr)
        except ValueError:
            raise ValueError('String %s cannot be converted to a number!' %numstr)

def score_mult_sing_sel_general(dfin, dfout, col, valscore):
    maxval = max(valscore.values())
    for v, sc in valscore.items():
        dfout.loc[dfin[col] == v, col] = np.divide(sc,maxval)
    dfout.loc[pd.isnull(dfin[col]), col] = 0

def score_mult_mult_sel_general(dfin, dfout, col, valscore):
    sumval = sum(valscore.values())
    option_s = [v for v in dfin[col].unique() if pd.notnull(v)]
    for o_str in option_s:
        dfout.loc[dfin[col] == o_str, col] = np.divide(sum([valscore[s] for s in o_str.split('#')]), sumval)
    dfout.loc[pd.isnull(dfin[col]), col] = 0

def score_thresh_general(dfin, dfout, col, thresh):
    dfin.loc[pd.isnull(dfin[col]), col] = 0
    colvals = dfin.loc[:,col]
    gr_arr = np.greater_equal(colvals, thresh)
    sm_arr = np.less(colvals, thresh)
    colvals = np.divide(colvals, thresh)
    nvals = np.multiply(sm_arr, colvals)
    hvals = gr_arr.astype(int)
    dfout.loc[:,col] = np.add(nvals, hvals)


def score_thresh_upper_lower_lim_low(dfin, dfout, col, threshL, threshH):
    dfin.loc[pd.isnull(dfin[col]), col] = 0
    colvals = dfin.loc[:,col]
    #gr_arr = np.logical_not(np.greater_equal(colvals, threshH))
    sm_arr = np.less_equal(colvals, threshL)
    between = np.logical_and(np.greater(colvals,threshL), np.less(colvals, threshH))
    #bools = np.logical_or(sm_arr, between).astype(int)
    colvals = np.divide(np.subtract(threshH, colvals), threshH-threshL)
    betvals = np.multiply(between, colvals)
    dfout.loc[:,col] = np.add(sm_arr.astype(int), betvals)


def score_thresh_upper_lower_lim_high(dfin, dfout, col, threshL, threshH):
    dfin.loc[pd.isnull(dfin[col]), col] = 0
    colvals = dfin.loc[:,col]
    gr_arr = np.greater_equal(colvals, threshH)
    #sm_arr = np.less_equal(colvals, threshL)
    between = np.logical_and(np.greater(colvals,threshL), np.less(colvals, threshH))
    colvals = np.divide(np.subtract(colvals, threshL), threshH-threshL)
    #hvals = gr_arr.astype(int)
    #lvals = sm_arr.astype(int)
    betvals = np.multiply(between, colvals)
    dfout.loc[:,col] = np.add(gr_arr.astype(int), betvals)


# F_TR_G = 'thresh_general'
# F_MC_MS_G = 'multi_choice_multi_select'
# F_MC_SS_G = 'multi_choice_single_select'
# F_TR_UP_LM_L = 'thresh_upper_lower_lim_low'
# F_TR_UP_LM_H = 'thresh_upper_lower_lim_high'

FUNCS = {
        #: score_thresh_general,
        FR_T_MULT_SEL: score_mult_mult_sel_general,
        FR_T_STR_NR: score_mult_sing_sel_general,
        #F_TR_UP_LM_L: score_thresh_upper_lower_lim_low,
        #F_TR_UP_LM_H: score_thresh_upper_lower_lim_high,
        }

def score(df, dfout, attrd):
    dq = deque()
    dq.append(attrd)
    while len(dq) > 0:
        atr = dq.pop()
        for tag, tagd in atr.items():
            if tag == 'weight':
                continue
            frmt = tagd.get('format', False)
            if frmt:
                print(tag)
                if frmt == FR_T_NUM or frmt == FR_T_TIME:
                    thresh = tagd.get('threshold', False)
                    # calculate score using threshold formula.
                    print('Threshold: ', thresh, ', type: ', type(thresh))
                    score_thresh_general(df, dfout, tag, thresh)
                else:
                    values = tagd.get('values', False)
                    print('Values: ', values)
                    # calculate score using multiselect or single select.
                    FUNCS[frmt](df, dfout, tag, values)
            else:
                dq.append(tagd)


if __name__ == '__main__':
    import os

    from cleaning_pipeline import from_yaml

    svm_dir = os.getenv('SVM_DIR')
    attrd = from_yaml(os.path.join(svm_dir, 'yaml/assigned/anganwadi.yaml'))

    df = pd.read_csv(os.path.join(svm_dir, 'csv/cleaned/anganwadi.csv'))

    outdf = pd.DataFrame(columns=df.columns)
    score(df, outdf, attrd)

    outdf.to_csv('~/anganwadi_output.csv', index=False)
    print(outdf.describe())
