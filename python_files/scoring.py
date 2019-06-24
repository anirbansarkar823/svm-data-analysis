import pandas as pd
import numpy as np


def str_to_num(numstr):
    try:
        return int(numstr)
    except ValueError:
        try:
            return float(numstr)
        except ValueError:
            raise ValueError('String %s cannot be converted to a number!' %numstr)

def score_mult_sing_sel_general(dfin, dfout, col, valscore, maxval):
    for v, sc in valscore.items():
        dfout.loc[dfin[col] == v, col] = np.divide(sc,maxval)
    dfout.loc[pd.isnull(dfin[col]), col] = 0

def score_mult_mult_sel_general(dfin, dfout, col, valscore, sumval):
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


F_TR_G = 'thresh_general'
F_MC_MS_G = 'multi_choice_multi_select'
F_MC_SS_G = 'multi_choice_single_select'
F_TR_UP_LM_L = 'thresh_upper_lower_lim_low'
F_TR_UP_LM_H = 'thresh_upper_lower_lim_high'

FUNCS = {
        F_TR_G: score_thresh_general,
        F_MC_MS_G: score_mult_mult_sel_general,
        F_MC_SS_G: score_mult_sing_sel_general,
        F_TR_UP_LM_L: score_thresh_upper_lower_lim_low,
        F_TR_UP_LM_H: score_thresh_upper_lower_lim_high,
        }

# ATTRS_VARS_FUNC = {
#         'observation': {
#             'accessibility': {
#                 'times_visited_before_open': F_TR_G,
#                 'type_road_available_to_asset': F_MC_SS_G,
#                 'distance_travelled_to_avail_public_transport_in_km': F_TR_UP_LM_L, # pass lower limit as 1
#                 'type_of_mobile_network_available': F_MC_SS_G,
#                 'buses_to_asset': F_TR_G,
#                 },
#             'infrastructure': {
#                 'total_campus_area': F_TR_G,
#                 'type_of_security_available': F_MC_MS_G,
#                 'type_of_structure_of_asset': F_MC_SS_G,
#                 },
#             },
#         'general': {
#             'availability': {
#                 'working_days_of_facility': F_MC_MS_G,
#                 'working_hours_of_facility': F_TR_G,
#                 },
#             'employability': {
#                 'no_of_teachers_employed_in_facility': F_TR_G,
#                 'no_of_support_staff_employed_in_facility': F_TR_G,
#                 },
#             'water': {
#                 'drinking_water_source': F_MC_MS_G,
#                 'cost_per_litre_bottled_water_in_rupees': F_TR_UP_LM_L,
#                 },
#             'toilet': {
#                 'toilets_available_for_public': F_MC_SS_G,
#                 'toilets_available_separately_per_gender': F_MC_SS_G,
#                 'running_water_available_in_toilets': F_MC_SS_G,
#                 'soap_for_handwash_available': F_MC_SS_G,
#                 },
#             'waste_management': {
#                 'facility_waste_management': F_MC_MS_G,
#                 },
#             'general_cleanliness': {
#                 'premises_cleaned_with_disinfectant_regularly': F_MC_SS_G,
#                 'frequency_cleaning_with_disinfectant_per_week': F_MC_SS_G,
#                 },
#             'energy': {
#                 'grid_connection_for_energy_supply': F_MC_SS_G,
#                 'hours_per_day_with_power_cuts': F_TR_UP_LM_L, # pass lower limit as 0
#                 },
#             'alternate_energy':{
#                 'alternative_energy_source_available': F_MC_MS_G,
#                 'alternative_energy_source_per_day_in_hours': F_TR_UP_LM_H, # pass lower limit as 0
#                 },
#             'communication': {
#                 'mobile_network_service_providers_available': F_MC_MS_G,
#                 },
#             'record_maintenance': {
#                 'maintain_records_for_operations': F_MC_MS_G,
#                 },
#             'govt_support': {
#                 'areas_getting_support_from_govt_agencies_facility': F_MC_MS_G,
#                 'areas_getting_support_from_govt_agencies_students': F_MC_MS_G,
#                 },
#             'educational_material': {
#                 'textbooks_source_for_children': F_MC_MS_G,
#                 'curriculum_for_classes': F_MC_MS_G,
#                 },
#             'digital_technology': {
#                 'digital_tools_for_teaching': F_MC_SS_G,
#                 },
#             'health': {
#                 'checkups_or_medical_facilities_available': F_MC_SS_G,
#                 'frequency_of_checkups': F_MC_SS_G,
#                 'any_meals_served': F_MC_SS_G,
#                 'nutritional_value_monitored': F_MC_SS_G,
#                 },
#             'facilities': {
#                 'recreation_and_playing_material_kids': F_MC_SS_G,
#                 'kind_residential_facilities': F_MC_MS_G,
#                 'classrooms_count': F_TR_UP_LM_H, # pass lower limit as 0
#                 },
#             'educational_statistics': {
#                 'student_enrolled': F_TR_UP_LM_H, # pass lower limit as 0
#                 'co-curricular_activities_for_students': F_MC_MS_G,
#                 'percentage_drop_outs': F_MC_SS_G
#                 'reason_dropouts': F_MC_MS_G,
#                 },
#             'disaster_preparedness': {
#                 'disaster_management_courses_or_drills': F_MC_SS_G,
#                 },
#             },
#         'specific': {
#                 'diversity': {
#                     'no_of_women_served': F_MC_SS_G,
#                     },
#                 'govt_support': {
#                     'timely_supplies_of_govt_goods': F_MC_SS_G,
#                     'materials_the_govt_is_providing_fund': F_MC_MS_G,
#                     'source_of_supplies': F_MC_MS_G,
#                     },
#             },
#         }


def scoring(dfi, dfo, val_thresh_dict):
    def score(dict_elem, taglist):
        if type(dict_elem) != dict:
            col, score_fn = taglist[-1], FUNCS[dict_item]
            col_vals_thresh = val_thresh_dict[col]
            if dict_elem == F_TR_G:
                thresh = col_vals_thresh['threshold']
                score_fn(dfi, dfo, col, thresh)
            elif dict_item == F_TR_UP_LM_L or dict_item == F_TR_UP_LM_H:
                threshL, threshH = (str_to_num(t) for t in col_vals_thresh['threshold'])
                score_fn(dfi, dfo, col, threshL, threshH)
            elif dict_item == F_MC_MS_G:
                vals = col_vals_thresh['values']
                score_fn(dfi, dfo, col, vals, sum(v for v in vals.values()))
            elif dict_item == F_MC_SS_G:
                vals = col_vals_thresh['values']
                score_fn(dfi, dfo, col, vals, max(v for v in vals.values()))
            else:
                raise NotImplementedError('Scoring function %s is not implemented!' %dict_item)

        else:
            for tag,val in dict_item.items():
                out_dict[tag] = dict()
                score(val, taglist + [tag])
    score(ATTRS_VARS_FUNC,[])

# def score_sheet_gen(df, attr_vars_dict):
#     def gen(attrd):
#         # elems = [e for e in dfrem[seq[0]] if pd.notnull(e)]
#         # entity_score = np.zeros(len(elems))
#         # for i,e in enumerate(elems):
#         #     elem_score = gen(dfrem.loc[dfrem[seq[0]] == e,:],seq[1:])
#         #     entity_score[i] = elem_score
#         #     # to be continued
#         if type(list(attrd.values()[0])) != dict:
#             col = list(attrd.keys())[0]




