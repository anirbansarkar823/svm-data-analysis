""" file: ./cleaning_pipeline.py
A python module for creating a pipeline for the task of
cleaning svm data.

The sequence of events are as follows:
    1. grouping columns to sections: Read indices from
        YAML file and group columns into sections.
    2. deletion of columns: Read indices from YAML file
        delete columns from the dataframe.
    3. maintain consistency between grouping and deletion.
    4. cleaning of column entries: Match the column data
        based on a general regex and then select 
        formatting based on the contents.
    5. manual checking for consistence: Left to the
        admin.
"""

import re

from collections import OrderedDict
from collections import deque

import pandas as pd

from common import to_yaml, from_yaml, del_cols
from common import REGEX, FR_T_MULT_SEL, \
        FR_T_STR_NR, FR_T_TIME, FR_T_NUM


def format_multi_choice_multi_select(df, col):
    vals = [v for v in df[col].unique() if pd.notnull(v)]
    for o_val in vals:
        n_val = o_val.strip().lstrip('[').rstrip(']')
        n_val = '#'.join([s.strip('"').strip().lower() \
                        for s in n_val.split(',')])
        df.loc[df[col]==o_val,col] = n_val


def format_time(df, col):
    vals = [v for v in df[col] if pd.notnull(v)]
    for o_val in vals:
        digit_list = re.findall(REGEX['time'], o_val)
        digit_list = list(map(int, digit_list))
        start_hr, start_min = digit_list[0], digit_list[1]
        end_hr, end_min = digit_list[2], digit_list[3]
        if end_hr < 12 and start_hr < 12 and start_hr < end_hr:
            hours = end_hr-start_hr
        elif end_hr < 12 and start_hr < 12 and end_hr < start_hr:
            hours = 12+end_hr-start_hr
        elif end_hr >= 12 and start_hr < 12:
            hours = end_hr-start_hr
        elif end_hr < 12 and start_hr >= 12:
            hours = 24+end_hr-start_hr
        else:
            hours = 0
        df.loc[df[col]==o_val,col] = 60*hours+(end_min-start_min)


def format_normal_string(df, col):
    vals = [v for v in df[col].unique() if pd.notnull(v)]
    for v in vals:
        if len(v) == 0:
            df.loc[df[col]==v, col] = pd.np.nan
        else:
            df.loc[df[col]==v,col] = v.lower()


FUNCS = {
        FR_T_NUM: lambda df, col: None,
        FR_T_MULT_SEL: format_multi_choice_multi_select,
        FR_T_STR_NR: format_normal_string,
        FR_T_TIME: format_time,
        }


def group_sec_and_format(df, secd):
    '''group the columns in the dataframe *df* into
    sections given in *secd*.

    @df : input dataframe.
    @secd : see the associated YAML format.
    @return: *list*,*OrderedDict*, list of questions
        and dictionary of grouping.
    '''
    grouped_sec, dq = OrderedDict(), deque()
    dq.append((secd, grouped_sec))
    ques_list = []

    while len(dq) > 0:
        scd, grpd = dq.pop()
        for tag, tagd in scd.items():
            if tagd.get('start'):
                start, end = tagd['start'], tagd['end']
                for ques in df.columns[start:end]:
                    if not grpd.get(tag):
                        grpd[tag] = OrderedDict()
                    if not grpd.get(ques):
                        grpd[tag][ques] = OrderedDict()
                    ques_list.append(ques)
                    if not(str(df[ques].dtype) in ['int64', 'float64']):
                        vals = [v for v in df[ques].unique()
                                if pd.notnull(v)]
                        frmt = None
                        if len(vals) > 0:
                            if type(vals[0]) == float or type(vals[0]) == int:
                                frmt = FR_T_NUM
                            elif vals[0].strip().startswith('['):
                                frmt = FR_T_MULT_SEL
                            elif len(re.findall(REGEX[FR_T_TIME], vals[0])) == 4:
                                frmt = FR_T_TIME
                            else:
                                frmt = FR_T_STR_NR
                            grpd[tag][ques]['format'] = frmt
                            FUNCS[frmt](df, ques)
                        else:
                            grpd[tag][ques] = None
                            ques_list.pop()
                    else:
                        grpd[tag][ques]['format'] = FR_T_NUM
            else:
                grpd[tag] = OrderedDict()
                dq.append((tagd,grpd[tag]))
    return ques_list, grouped_sec


def del_cols_group_sec_and_format(df, quesi, colsdel, secd, inplace=False):
    '''delete and group columns.'''
    ques_list, grouped_sec = group_sec_and_format(df, secd)
    ques_del = (set(df.columns[quesi:]) - set(ques_list))
    todelete = colsdel + list(ques_del)
    del_cols(df, todelete, inplace)
    return ques_list, grouped_sec


def clean(df, attrd):
    filter_attr = attrd['filter']['attribute']
    filter_val = attrd['filter']['value']
    df = df.loc[df[filter_attr] == filter_val, :].copy()
    ques_i = attrd['questions_starting_index']
    grouping = attrd['grouping']
    colsdel = [df.columns[i] for i in attrd['delete_cols']]

    ques_list, groupedd = del_cols_group_sec_and_format(df, ques_i, colsdel, grouping, inplace=True)

    labels = ['correct', 'rename', 'attr_seq', 'reformat', 'sections']
    values = ['# to be filled manually #' for i in range(4)] + [groupedd]
    return OrderedDict(zip(labels, values)),df


if __name__ == '__main__':
    import os
    import argparse
    import ntpath

    parser = argparse.ArgumentParser(description="Clean data in the input csv file and generate output csv and yaml files.")
    parser.add_argument('-df', help='Path to the input csv file')
    parser.add_argument('-yml', help='Path to the input yaml template.')
    parser.add_argument('-s', help='Separator used in the csv file')

    args = parser.parse_args()

    csv_dir = os.getenv('CSV_PR')
    yml_dir = os.getenv('YML_ATR')

    if not (csv_dir and yml_dir):
        print('Output directories not set')
        exit()
        
    csvfile, sep, ymlfile = args.df, args.s, args.yml
    csvfilename = ntpath.basename(csvfile).split('.')[0] + '.csv'
    ymlfilename = ntpath.basename(ymlfile).split('.')[0] + '.yaml'
    out_yaml_file = os.path.join(yml_dir, ymlfilename)
    out_csv_file = os.path.join(csv_dir, csvfilename)

    out_yaml_exists = os.path.isfile(out_yaml_file)
    out_csv_exists = os.path.isfile(out_csv_file)

    if out_yaml_exists:
        print(out_yaml_file, 'exists!')
    elif out_csv_exists:
        print(out_csv_file, 'exists!')
    else:

        df = pd.read_csv(csvfile, sep=sep)
        attrd = from_yaml(ymlfile)
        groupped, df = clean(df, attrd)
        df.to_csv(out_csv_file, sep=',', na_rep='N/A', index=False)
        to_yaml(out_yaml_file, groupped)
