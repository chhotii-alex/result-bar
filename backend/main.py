from typing import Union
from sqlalchemy import create_engine, text
import pandas as pd
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pprint import pp
from connect import connectionString
from scipy.stats import binomtest

app = FastAPI()

class QueryParams(BaseModel):
    test_name: str
    params: dict[str, list[str]]

eng = create_engine(connectionString)

origins = ["http://localhost:5173"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/testlist")
def get_test_list():
    df = pd.read_sql("SELECT * from tests_lookup", eng)
    results = { row[1]['dx'] : row[1]['table_name'] for row in df.iterrows()}
    return results

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

@app.post("/data/labbrowser")
def get_data(query_params: QueryParams):
    data = {"dx" : query_params.test_name, "label": "all", 'data': []}
    params = query_params.params
    with eng.connect() as con:
        for label in ['positive', 'negative']:
            data['data'].append(data_for_label(
                query_params.test_name,
                label,
                "result='%s'" % label,
                list(params.keys()),
                params,
                con
            ))
    # Calculate confidence intervals:
    #     see https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats._result_classes.BinomTestResult.proportion_ci.html
    totals = {}
    remaining_keys = list(params.keys())
    for result in data['data']:
        add_to_totals(totals, remaining_keys, result['data'])
    for result in data['data']:
        distribute_totals(totals, remaining_keys, result['data'])
    return data

def distribute_totals(totals, remaining_keys, data):
    for result in data:
        if type(result['data']) == list:
            distribute_totals(totals[result['label']],
                          remaining_keys[1:],
                          result['data'])
        else:
            result['total'] = totals[result['label']]
            stat_result = binomtest(k=result['data'], n=result['total'], p=0.1)
            ci = stat_result.proportion_ci()
            result['ci_low'] = ci.low
            result['ci_high'] = ci.high

def add_to_totals(totals, remaining_keys, data):
    for result in data:
        if type(result['data']) == list:
            if result['label'] not in totals:
                totals[result['label']] = {}
            add_to_totals(totals[result['label']],
                          remaining_keys[1:],
                          result['data'])
        else:
            if result['label'] not in totals:
                totals[result['label']] = 0
            totals[result['label']] += result['data']

def data_for_label(dx, label, query, remaining_keys, params, con):
    result = {"label": label}
    if remaining_keys:
        result['data'] = []
        key = remaining_keys[0]
        levels = params[key]
        for level in splits[key].splits:
            if level.value in levels:
                new_query = "%s AND %s" % (query,
                                           level.whereClause)
                result['data'].append(data_for_label(
                    dx,
                    level.valueDisplayName,
                    new_query,
                    remaining_keys[1:],
                    params,
                    con
                ))
    else:
        query = """SELECT count(*) from results_public
           WHERE dx = '%s'
           AND %s""" % (dx, query)
        result['data'] = con.execute(text(query)).scalar_one()
    return result
