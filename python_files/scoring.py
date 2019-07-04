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
    dfvalues = [v for v in df[col].unique()]
    valseries = pd.Series(np.zeros(len(dfin[col])), index=dfin.index)
    for v in dfvalues:
        vscore = np.divide(valscore.get(v,0), maxval)
        valseries += np.multiply(dfin[col] == v, vscore)
    dfout.loc[:,col] = valseries


def score_mult_mult_sel_general(dfin, dfout, col, valscore):
    sumval = sum(valscore.values())
    option_s = [v for v in dfin[col].unique() if pd.notnull(v)]
    valseries = pd.Series(np.zeros(len(dfin[col])), index=dfin.index)
    for vstr in option_s:
        if pd.notnull(vstr):
            vscore = np.divide(sum(valscore[v] for v in vstr.split('#')), sumval)
        else:
            vscore = 0
        valseries += np.multiply(dfin[col]==vstr, vscore)

    dfout.loc[:,col] = valseries


def score_thresh_general(dfin, dfout, col, thresh):
    valseries = pd.Series(np.zeros(len(dfin[col])), index=dfin.index)
    valseries = np.add(valseries, dfin[col] >= thresh)
    score = np.divide(df[col], thresh)
    valseries = np.add(valseries, np.multiply(df[col] < thresh, score))
    dfout.loc[:,col] = valseries
    dfout.loc[pd.isnull(valseries), col] = 0


def score_thresh_upper_lower_lim_low(dfin, dfout, col, threshL, threshH):
    valseries = pd.Series(np.zeros(len(dfin[col])), index=dfin.index)
    valseries = np.add(valseries, dfin[col] <= threshL)
    inbetween = np.logical_and(dfin[col] > threshL, dfin[col] < threshH)
    high_minus_val = np.subtract(threshH, dfin[col])
    high_minus_low = threshH - threshL
    score = np.divide(high_minus_val, high_minus_low)
    valseries = np.add(valseries, np.multiply(inbetween, score))
    dfout.loc[:,col] = valseries
    dfout.loc[pd.isnull(valseries), col] = 0


def score_thresh_upper_lower_lim_high(dfin, dfout, col, threshL, threshH):
    valseries = pd.Series(np.zeros(len(dfin[col])), index=dfin.index)
    valseries = np.add(valseries, dfin[col] >= threshH)
    inbetween = np.logical_and(dfin[col] > threshL, dfin[col] < threshH)
    val_minus_low = np.subtract(dfin[col], threshL)
    high_minus_low = thresh_H - threshL
    score = np.divide(val_minus_low, high_minus_low)
    valseries = np.add(valseries, np.multiply(inbetween, score))
    dfout.loc[:,col] = valseries
    dfout.loc[pd.isnull(valseries), col] = 0
    

def set_prec(df, start, decimals=4):
    for col in df.columns[start:]:
        df.loc[:,col] = np.round(df[col], decimals=decimals)


FUNCS = {
        #: score_thresh_general,
        FR_T_MULT_SEL: score_mult_mult_sel_general,
        FR_T_STR_NR: score_mult_sing_sel_general,
        #F_TR_UP_LM_L: score_thresh_upper_lower_lim_low,
        #F_TR_UP_LM_H: score_thresh_upper_lower_lim_high,
        }


def score(df, dfout, attrd):
    dq, ques = deque(), []
    dq.append(attrd)
    while len(dq) > 0:
        atr = dq.pop()
        for tag, tagd in atr.items():
            if tag == 'weight':
                continue
            print(tag)
            frmt = tagd.get('format', False)
            if frmt:
                ques.append(tag)
                if frmt == FR_T_NUM or frmt == FR_T_TIME:
                    thresh = tagd.get('threshold', False)
                    if thresh:
                        thresh = [str_to_num(t.strip()) for t in str(thresh).strip().split('#')]
                        if len(thresh) == 1:
                            # calculate score using threshold formula.
                            score_thresh_general(df, dfout, tag, thresh[0])
                        elif len(thresh) == 2:
                            if thresh[0] > thresh[1]:
                                high, low = thresh[0], thresh[1]
                                score_thresh_upper_lower_lim_high(df, dfout, tag, low, high)
                            else:
                                low, high = thresh[0], thresh[1]
                                score_thresh_upper_lower_lim_low(df, dfout, tag, low, high)
                        else:
                            raise ValueError('Threshold not defined correctly')

                else:
                    values = tagd.get('values', False)
                    # calculate score using multiselect or single select.
                    FUNCS[frmt](df, dfout, tag, values)
            else:
                dq.append(tagd)
    return ques


def gen_score_sheet(df, attrd, assetname, attrseq=['sections', 'variables', 'sub_parameters', 'questions']):
    variable_list = []
    def gen(prevtag, currd):
        if currd.get('format'):
            return
        for tag, tagd in currd.items():
            if tag == 'weight' or tag in attrseq:
                if tag in attrseq:
                    gen(prevtag, tagd)
                    multiplier = np.divide(1,100) if tag in attrseq[:3] else 1
                    prevtag_score = pd.Series(np.zeros(len(df)), index=df.index)
                    for k in tagd.keys():
                        if tag == 'variables':
                            variable_list.append(k)
                        weighted = np.multiply(tagd[k]['weight'], df[k])
                        prevtag_score = np.add(prevtag_score, np.multiply(multiplier, weighted))
                    # df.assign(prevtag = prevtag_score)
                    df.loc[:,prevtag] = prevtag_score
                continue
            else:
                gen(tag, tagd)
    gen(assetname, {'sections': attrd['sections']})
    return variable_list


if __name__ == '__main__':
    import os
    import argparse
    import ntpath

    from common import from_yaml, df_to_csv

    parser = argparse.ArgumentParser(description="Clean data in the input csv file and generate output csv and yaml files.")
    parser.add_argument('-df', help='Path to the input csv file')
    parser.add_argument('-yml', help='Path to the input yaml template.')
    parser.add_argument('-s', help='Separator used in the csv file')

    args = parser.parse_args()

    csv_dir = os.getenv('CSV_SC')

    if not (csv_dir):
        print('Output directories not set')
        exit()
        
    csvfile, sep, ymlfile = args.df, args.s, args.yml
    filename = ntpath.basename(csvfile).split('.')[0]
    csvfilename = filename + '.csv'
    variablesheet = os.path.join(csv_dir, filename + '_variable.csv')
    out_csv_file = os.path.join(csv_dir, csvfilename)

    out_csv_exists = os.path.isfile(out_csv_file)

    if out_csv_exists:
        print(out_csv_file, 'exists!')
    else:
        attrd = from_yaml(ymlfile)
        df = pd.read_csv(csvfile)
        q_start = attrd['ques_start_index']
        outdf = pd.DataFrame(columns=df.columns)
        non_ques = df.columns[:q_start]
        for col in non_ques:
            outdf.loc[:,col] = df[col]
        ques = score(df, outdf, {'sections': attrd['sections']})
        drop_cols = [v for v in df.columns if not (v in ques or v in non_ques)]
        outdf.drop(columns=drop_cols, axis=1, inplace=True)

        assetname = 'overall score'
        variable_list = gen_score_sheet(outdf, attrd, assetname)

        set_prec(outdf, q_start)

        variabledf = outdf[list(df.columns[:q_start])+variable_list+[assetname]]

        df_to_csv(outdf, out_csv_file)
        df_to_csv(variabledf, variablesheet)
