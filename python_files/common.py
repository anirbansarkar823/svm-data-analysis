""" file: ./common.py
File containing common construct used by other scripts.
"""

import yaml
import pandas as pd

from collections import OrderedDict


FR_T_TIME = 'time'
FR_T_MULT_SEL = 'multi_select'
FR_T_STR_NR = 'normal_string'
FR_T_NUM = 'number'

REGEX = {
        FR_T_TIME: '[0-9]{1,2}',
        }


yaml.add_representer(OrderedDict,
        lambda dmpr, dt: dmpr.represent_dict(dt.items()))
yaml.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
        lambda ldr, nd: OrderedDict(ldr.construct_pairs(nd)))
yaml.add_constructor(u'tag:yaml.org,2002:bool',
        lambda self, node: self.construct_scalar(node))


def to_yaml(fname, data):
    with open(fname, 'w', encoding='utf-8') as f:
        f.write(yaml.dump(data, indent=6, default_flow_style=False))


def from_yaml(fname):
    with open(fname, 'r', encoding='utf-8') as f:
        s = f.read()
        return yaml.load(s)


def del_cols(df, cols, inplace=False):
    '''delete the columns from the dataframe *df* whose
    column indices are given in *cols*. The changes will
    be inplace or will return a modified copy base on the
    flag *inplace*.

    @df : input dataframe.
    @cols : list containing the column indices.
    @inplace : boolean flag.
    @return : None if *inplace* True else None.
    '''
    df.drop(columns=cols, axis=1, inplace=inplace)
