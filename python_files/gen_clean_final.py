import itertools

import pandas as pd

from collections import OrderedDict, deque

from common import FR_T_STR_NR, FR_T_TIME, \
        FR_T_MULT_SEL, FR_T_NUM


def reformat_df(df, col, frmt):
    if frmt == FR_T_TIME or FR_T_NUM:
        df.loc[:,col] = pd.to_numeric(df[col])
    elif frmt == FR_T_MULT_SEL:
        unique = [v for v in df[col].unique()
                if pd.notnull(v)]
        for v in unique:
            new_v = v
            if ',' in v:
                new_v = '#'.join(v.strip().split(','))
                print(new_v)
            df.loc[df[col] == v, col] = new_v


REFORMAT = {
        FR_T_STR_NR : lambda df, col: None,
        FR_T_NUM: lambda df, col: reformat_df(df, col, FR_T_NUM),
        FR_T_TIME: lambda df, col: None,
        FR_T_MULT_SEL: lambda df, col: None,
        }

TAG_FOR_FRMT = {
        FR_T_STR_NR: 'values',
        FR_T_MULT_SEL: 'values',
        FR_T_NUM: 'threshold',
        FR_T_TIME: 'threshold',
        }

STR_FOR_TAG = {
        'values' :'',
        'threshold': '',
        }


def correct_df(df, cols_correct_dat):
    cols_correct_dat = cols_correct_dat or {}
    for col, corr_dat in cols_correct_dat.items():
        o_val = list(corr_dat.keys())[0]
        df.loc[df[col] == o_val,col] = corr_dat[o_val]

def rename_cols(df, colsd):
    colsd = colsd or {}
    if len(colsd) > 0:
        df.rename(columns=colsd, inplace=True)


def gen_final_yaml_for_weights(df, attrd, attrseq, refrmtd):
    weightsd, dq = OrderedDict(), deque()
    dq.append((0, attrd, weightsd))
    while len(dq) > 0:
        lvl, atrd, nptr = dq.pop()
        label = attrseq[lvl]
        if len(atrd) <= 0:
            continue

        if not nptr.get(label):
            nptr[label] = OrderedDict()

        for tag, tagd in atrd.items():
            frmt = tagd.get('format')
            if frmt:
                print(tag)
                if refrmtd:
                    reformat = refrmtd.get(tag)
                    frmt = reformat or frmt
                    REFORMAT[frmt](df, tag)
                inner_tag = TAG_FOR_FRMT[frmt]
                val_str = STR_FOR_TAG[inner_tag]
                
                if not nptr[label].get(tag):
                    nptr[label][tag] = OrderedDict()
                nptr[label][tag]['weight'] = ''
                nptr[label][tag]['format'] = frmt
                nptr[label][tag][inner_tag] = val_str
                if frmt in [FR_T_STR_NR, FR_T_MULT_SEL]:
                    vals = set(v for v in df[tag].unique()
                            if pd.notnull(v))
                    if frmt == FR_T_MULT_SEL:
                        join_func = itertools.chain.from_iterable
                        vals = set(join_func(v.split('#') for v in vals))
                    valued = OrderedDict((str(v), val_str) for v in vals)
                    nptr[label][tag][inner_tag] = valued
            else:
                nptr[label][tag] = OrderedDict()
                nptr[label][tag]['weight'] = ''
                dq.append((lvl+1,tagd, nptr[label][tag]))

    return weightsd


if __name__ == '__main__':
    import argparse
    import os
    import ntpath
    
    
    from common import to_yaml, from_yaml, df_to_csv


    parser = argparse.ArgumentParser(description='Correct data in the processed csv data and generated YAML file for weights assignment.')
    parser.add_argument('-df', help='Path to the processed csv file to be corrected')
    parser.add_argument('-yml', help='Path to the YAML file with template and correction data.')
    parser.add_argument('-s', help='Separator used in the csv file.')

    args = parser.parse_args()
    csv_dir = os.getenv('CSV_CLN')
    yml_dir = os.getenv('YML_WTV')

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
        attrd_corr = from_yaml(ymlfile)
        corr_data = attrd_corr['correct']
        colsd = attrd_corr['rename']
        attr_seq = attrd_corr['attr_seq']
        reformatd = attrd_corr['reformat']
        attrd = attrd_corr['sections']

        correct_df(df, corr_data)
        rename_cols(df, colsd)
        df_to_csv(df, out_csv_file)
        to_yaml(out_yaml_file,
                gen_final_yaml_for_weights(df, attrd, attr_seq, reformatd))
