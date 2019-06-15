import pandas as pd
from datetime import datetime

from svm_doc_templates import *

def select_attr_rows(dframe):                  
     dframe = dframe.iloc[:,:12].copy()
     # rename columns
     for col in dframe.columns[:]:
         dframe.rename(columns={col:col.strip().lower().replace(' ','_')}, inplace=True)
     # drop unwanted columns
     dframe.drop([dframe.columns[2],dframe.columns[9],dframe.columns[10]], axis=1, inplace=True)
     # rename options column
     dframe.rename(columns={dframe.columns[8]:dframe.columns[8].split('_')[0]}, inplace=True)
     # select rows
     index = dframe.loc[dframe.section=='Specific'].index[0]
     return dframe.iloc[index:,:].copy()


def clean_data_entries(df):
    for col in df.columns:
        vals = [v for v in df[col].unique() if pd.notnull(v)]
        for v in vals:
            if '-' in vals:
                vstr = '-'.join(v.split('-'))
            else:
                vstr = v
            df.loc[df[col] == v, col] = ' '.join(vstr.strip().strip('*').strip('#').split())
    return df


def clean_multiple_choice(df):
    res_type = ['Multiple Choice', 'Binary']
    for t in res_type:
        indices = df.loc[df.response_type==t].index
        for i in indices:
            choice = [df.loc[i,'options']]
            j, i = i, i+1
            while pd.isnull(df.loc[i,'response_type']) and pd.notnull(df.loc[i,'options']):
                choice.append(df.loc[i,'options'].strip())
                df.drop(i,inplace=True)
                i += 1
            # print(choice)
            df.loc[j,'options'] = '#'.join(choice)
    return df


def format_selection(df):
    df.loc[df.response_type=='Text box','response_type'] = 'Text Box'
    res_type = ['Multiple Choice', 'Binary']
    for t in res_type:
        if t == 'Binary':
            df.loc[df.response_type == t, 'condition'] = 'Single Select'
        else:
            for i in df.loc[df.response_type==t].index:
                df.loc[i,'condition'] = df.loc[i,'condition'].split('-')[-1].strip()
    return df

def fill_cols(dframe, cols_dict):
    for col, val in cols_dict.items():
        dframe.loc[:,col] = val
    return dframe


def fill_cols_seq(df, cols_seq):
    def fill(i, df_):
        if i > len(cols_seq)-1:
            return
        vals = [v for v in df_[cols_seq[i]].unique()
                if pd.notnull(v)]
        for v in vals:
            index = df_.loc[df_[cols_seq[i]]==v].index[0]
            j = index + 1
            while j < df_.index[-1]:
                if j in df_.index:
                    if pd.notnull(df_.loc[j,cols_seq[i]]):
                        break
                    df.loc[j,cols_seq[i]] = v
                j += 1
            fill(i+1,df_.loc[index:j, :])
    fill(0,df.copy())
    return df


def remove_unwanted_rows(df):
    wanted = ['Binary','Text Box', 'Multiple Choice']
    unwanted_res_t = [t for t in df.response_type.unique()
            if not t in wanted]
    for t in unwanted_res_t:
        df.drop(df.loc[df.response_type==t].index,inplace=True)
    return df


def remove_empty_row(df):
    return df.drop(df.loc[pd.isnull(df.question)].index)

def clean_dframe(dframe, cols_dict):
    dframe = select_attr_rows(dframe)
    dframe = clean_data_entries(dframe)
    dframe = clean_multiple_choice(dframe)
    dframe = remove_empty_row(dframe)
    dframe = fill_cols(dframe, cols_dict)
    dframe = fill_cols_seq(dframe,['section','variable','sub_parameter'])
    dframe = format_selection(dframe)
    dframe = remove_unwanted_rows(dframe)
    return dframe


def generate_doc(dframe):
    assets = dframe.asset_name.unique()
    for ast in assets:
        adf = dframe.loc[dframe.asset_name == ast]
        variables = adf.variable.unique()
        v_list = LATEX_UNORDERED_LIST
        v_items = []
        v_an_list = []
        for v in variables:
            if pd.isnull(v):
                v, v_item = '', ''
            else:
                v_item = ''.join(['\\item ', v])

            v_ss = LATEX_SUB_SUB_SECTION.format(subsubsecname=v)
            v_df = adf.loc[adf.variable == v]
            sbp_list = LATEX_ORDERED_LIST
            sbp_items = []
            sbp_an_list = []
            attr_zip = zip(v_df.sub_parameter, v_df.question,
                    v_df.response_type, v_df.options, v_df.condition)
            for sbp, qs, rs_t, opt, cnd in attr_zip:
                if pd.isnull(sbp):
                    sbp_s = ''
                    sbp_s1 = ''
                else:
                    sbp_s = sbp + ':'
                    sbp_s1 = sbp
                sbp_item = ' '.join(['\\item', sbp_s, qs])
                sbp_items.append(sbp_item)
                sbp_an_item = LATEX_PARAGRAPH.format(
                        par_name=' '.join([sbp_s, qs]))
                p_bdy = LATEX_PAR_PARTS[rs_t][cnd]
                if rs_t == 'Multiple Choice':
                    optns = opt.strip().split('#')
                    optns_s = [' '.join([o, '&', str(i+1), '\\\\']) for i,o in enumerate(optns)]
                    optns_s = '\n'.join(optns_s+['\\hline'])
                    if cnd == 'Single Select':
                        p_bdy = p_bdy.format(items=optns_s,
                                eqn='\\singsel{%s}'%sbp_s1)
                    else:
                        p_bdy = p_bdy.format(items=optns_s,
                                eqn='\\multisel{%s}'%sbp_s1)
                elif cnd != 'Text-Alphanumeric':
                    p_bdy = p_bdy.format(par=sbp_s1)

                sbp_an_item = '\n'.join([sbp_an_item, p_bdy])
                sbp_an_list.append(sbp_an_item)

            sbp_list_s = sbp_list.format(items='\n'.join(sbp_items))
            sbp_an_list_s = '\n'.join(sbp_an_list)
            v_items.append('\n'.join([v_item,sbp_list_s]))
            v_an_list.append('\n'.join([v_ss, sbp_an_list_s]))

        v_list_s = v_list.format(items='\n'.join(v_items))
        v_an_list_s = '\n'.join(v_an_list)
        pr_dt = datetime.utcnow().strftime('%A %e %B %Y')
        doc_bdy = LATEX_DOC_HEAD.format(asset=ast, date=pr_dt,
                vertical=adf.vertical.unique()[0],
                doc_body='\n'.join([LATEX_SECTION_ATTR_QUES.format(var_list=v_list_s), LATEX_SECTION_OVERALL_SCOR, LATEX_SECTION_ATTR_SCOR_PROC.format(var_analysis=v_an_list_s)]))
        
        fname = ast.strip().lower().replace(' ', '_')
        fname = fname.replace('/','_and_')
        with open('.'.join([fname,'tex']), 'w') as f:
            f.write(doc_bdy)


