from typing import Union
from sqlalchemy import create_engine, text
import pandas as pd
import numpy as np
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pprint import pp
from connect import connectionString
from scipy.stats import binomtest
import statsmodels.api as sm

app = FastAPI()

class QueryParams(BaseModel):
    test_name: str
    params: dict[str, list[str]]

eng = create_engine(connectionString)

origins = ["http://localhost:5173",
           'http://10.35.162.181:5173',
           ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

gTestList = None

@app.get("/testlist")
def get_test_list():
    global gTestList
    if gTestList is None:
        df = pd.read_sql("SELECT * from tests_lookup", eng)
        gTestList = { row[1]['dx'] : row[1]['table_name'] for row in df.iterrows()}
    return gTestList

class PatientSplit:
    def __init__(self, variable, variableDisplayName):
        self.variable = variable
        self.variableDisplayName = variableDisplayName
        self.splits = []

    def addSplit(self, splitSpecifier):
        self.splits.append(splitSpecifier)

class PatientSplitSpecifier:
    def __init__(self, row, splits):
        variable = row['variable']
        if variable in splits:
            split = splits[variable]
        else:
            variableDisplayName = row['variabledisplayname']
            split = PatientSplit(variable, variableDisplayName)
            splits[variable] = split
        split.addSplit(self)
        self.value = row['value']
        self.valueDisplayName = row['valuedisplayname']
        self.noun = row['noun']
        self.modifier = row['modifier']
        self.adjective = row['adjective']
        self.whereClause = row['whereclause']
        self._checked = row['initiallychecked']


def get_variables_and_splits():
    splits = {}
    query = """SELECT variable, variableDisplayName,
                        value, valueDisplayName, noun, adjective,
                        modifier, whereClause,
                      initiallyChecked
                    FROM UIVars ORDER BY sort"""
    df = pd.read_sql(query, eng)
    for row in df.iterrows():
        PatientSplitSpecifier(row[1], splits)
    query = """SELECT short_name, description
       from comorbidity_lookup
       order by short_name
    """
    df = pd.read_sql(query, eng)
    for row in df.iterrows():
        tag = row[1]['short_name']
        description = row[1]['description']
        split = {
            "variable": tag,
            "variabledisplayname": description,
            "value": 'true_' + tag,
            "valuedisplayname": "Known %s" % description,
            "noun": None,
            "modifier": "with %s" % description,
            "adjective": None,
            "whereclause": tag + " = 1",
            "initiallychecked": False,
        }
        PatientSplitSpecifier(split, splits)
        split["value"] = 'false_' + tag
        split["valuedisplayname"] = "no known %s" % description
        split["modifier"] = "with no %s" % description
        split["whereclause"] = tag + " = 0"
        PatientSplitSpecifier(split, splits)
    items = []
    for variable in splits.keys():
        split = splits[variable]
        divisions = []
        for spec in split.splits:
            divisions.append(
                {"value": spec.value,
                 "valueDisplayName":spec.valueDisplayName,
                 "_checked":spec._checked,
                   })
        items.append(
            {"id": split.variable,
             "displayName" : split.variableDisplayName,
             "splits":divisions
               })
    return (items, splits)

cached_vars, splits = get_variables_and_splits()

@app.get("/variables")
def get_variables():
    return {
        "items" : cached_vars
    }

def make_feature_col_name(key, value):
    s = "%s_%s" % (key, value)
    return s.lower()

@app.post("/data/labbrowser")
def get_data_heirarchical(query_params: QueryParams):
    params = query_params.params
    pp(query_params.params)
    where_clause = "dx = '%s' " % query_params.test_name
    if get_test_list()[query_params.test_name] == 'results':
        table_name = 'results_public'
        where_clause += "AND result in ('positive', 'negative') "
        columns = ['result']
    else:
        table_name = 'quantresults_public'
        columns = ['result_value_num', 'result_value_log10']
    for key in list(params.keys()):
        levels = params[key]
        querying_all_levels = True
        for level in splits[key].splits:
            if level.value in levels:
                feature_col = make_feature_col_name(key, level.value)
                sql_col = '(%s) %s' % (level.whereClause, feature_col)
                columns.append(sql_col)
            else:
                querying_all_levels = False
        if not querying_all_levels:
            where_clause_fragments = [("(%s)" % level.whereClause) for level in splits[key].splits if level.value in levels]
            where_clause_frag = " OR ".join(where_clause_fragments)
            where_clause = "(%s) AND %s" % (where_clause_frag, where_clause)
    columns = ", ".join(columns)
    query = """SELECT %s from %s WHERE %s""" % (columns, table_name, where_clause)
    df = pd.read_sql(query, eng)
    results = dice_results(query_params.test_name, df, 'all', '', list(params.keys()), params, table_name == 'quantresults_public')
    return results

small_group_cutoff = 10

def dice_results(test_name, df, label, label_value, remaining_keys, params, is_quantitative):
    results = {'dx': test_name,
               'label': label,
               'query': label_value,
               'total': df.shape[0],
               'type': 'counts'}
    if df.shape[0] >= small_group_cutoff and remaining_keys:
        do_split = True
        data = []
        key = remaining_keys[0]
        levels = params[key]
        for level in splits[key].splits:
            if level.value in levels:
                feature_col = make_feature_col_name(key, level.value)
                split_count = df[feature_col].sum()
                assert df[feature_col].sum() == df[df[feature_col] == True].shape[0]
                if split_count < small_group_cutoff:
                    do_split = False
                    break
                data.append(dice_results(test_name, df[df[feature_col] == True],
                                         level.valueDisplayName, level.value, remaining_keys[1:], params, is_quantitative))
    else:
        do_split = False
    if not do_split:
        results['showTotal'] = True
        data = []
        for result in ['positive', 'negative']:
            results_split = {'dx': test_name,
                             'label': result,
                             'total': df.shape[0],
                             'type': 'counts',
                             'isLeaf': True,
                            }
            if is_quantitative:
                if result == 'positive':
                    conditional = df['result_value_num'] > 0.0
                    results_split['type'] = 'histogram'
                    results_split['histogram'] = histogram(df.loc[conditional, 'result_value_log10'])
                else:
                    conditional = df['result_value_num'] == 0.0
            else:
                conditional = df['result'] == result
            count = conditional.sum()
            results_split['data'] = int(count)
            if df.shape[0] > 0:
                stat_result = binomtest(k=count, n=df.shape[0], p=0.1)
                ci = stat_result.proportion_ci()
                results_split['ci_low'] = ci.low
                results_split['ci_high'] = ci.high
            data.append(results_split)
    results['data'] = data
    return results
    
@app.post("/data/labbrowser2")
def get_data(query_params: QueryParams):
    pp(query_params.params)
    params = query_params.params
    if get_test_list()[query_params.test_name] == 'results':
        table_name = 'results_public'
    else:
        table_name = 'quantresults_public'
    with eng.connect() as con:
        results = counts_for_label(
            query_params.test_name,
            'all',
            '',
            None,
            list(params.keys()),
            params,
            con,
            table_name
        )
    return results

def counts_for_label(dx, label, label_value, where, remaining_keys, params, con, table_name):
    result = {"label": label, 'query': label_value, 'dx': dx, 'type': 'counts', 'data': []}
    if remaining_keys:
        key = remaining_keys[0]
        levels = params[key]
        total = 0
        for level in splits[key].splits:
            if level.value in levels:
                if where is None:
                    new_where = level.whereClause
                else:
                    new_where = "%s AND %s" % (where,
                                           level.whereClause)
                level_results = counts_for_label(
                    dx,
                    level.valueDisplayName,
                    level.value,
                    new_where,
                    remaining_keys[1:],
                    params,
                    con,
                    table_name
                )
                total += level_results['total']
                result['data'].append(level_results)
        result['total'] = total
    else:
        total = 0
        for label in ['positive', 'negative']:
            data_type = 'counts'
            if table_name == 'results_public':
                condition = "result='%s'" % label
            else:
                if label == 'positive':
                    condition = "result_value_num>0.0"
                    data_type = 'histogram'
                else:
                    condition = "result_value_num=0.0"
            if where is None:
                new_where = condition
            else:
                new_where = "%s AND %s" % (where, condition)
            if data_type == 'counts':
                query = """SELECT count(*) from %s
                WHERE dx = '%s'
                AND %s""" % (table_name, dx, new_where)
                print(query)
                count = con.execute(text(query)).scalar_one()
            else:
                query = """SELECT result_value_log10 from %s
                  WHERE dx = '%s'
                  AND %s""" % (table_name, dx, new_where)
                print(query)
                with con.execution_options(stream_results=True,
                                            max_row_buffer=100).execute(
                                                text(query)) as r:
                    rows = [row.result_value_log10 for row in r]
                    if len(rows) > 0:
                        histogram_data = histogram(rows)
                    else:
                        histogram_data = None
                    count = len(rows)  
            total += count
            data_record = {
                'label': label, 'dx': dx, 'type': data_type, 'data': count}
            if data_type == 'histogram':
                data_record['histogram'] = histogram_data
            result['data'].append(data_record)
        for i in range(2):
            data_record = result['data'][i]
            data_record['total'] = total
            if data_record['data'] > 0:
                stat_result = binomtest(k=data_record['data'], n=total, p=0.1)
                ci = stat_result.proportion_ci()
                data_record['ci_low'] = ci.low
                data_record['ci_high'] = ci.high
        result['total'] = total    
    return result

def kernel_density(data, start=0.0, stop=11.0):
    data = np.asarray(data)[:, np.newaxis]
    numpoints = round((stop-start)/0.02)+1
    X = np.linspace(start, stop, numpoints)
    kde = sm.nonparametric.KDEUnivariate(data)
    kde.fit(kernel="gau", bw=0.25)
    density = kde.evaluate(X)
    density[0] = 0
    density[-1] = 0
    r = np.asarray([X, density]).transpose()
    return r

def histogram(data):
    if not len(data):
        return None
    density = kernel_density(data, start=0.0, stop=10.0)
    densityBinWidth = density[2][0] - density[1][0]
    halfBin = densityBinWidth/2
    total = len(data)
    return [
        {"viralLoadLog": density[i][0],
         "viralLoadLogMin": density[i][0] - halfBin,
         "viralLoadLogMax": density[i][0] + halfBin,
         "count": density[i][1]*total*2}
        for i
        in range(density.shape[0]) ]
