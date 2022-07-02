import pandas as pd
import os
import boto3
import json
import decimal
import sys
from bs4 import BeautifulSoup
import requests
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError

masterCols=['B','N','1','2','3','4','M','R','T','W','?']
masterValues=[0,0,0,0,0,0,0,0,0,0,0]

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('pubchem_ct_annos')

def get_cid(cas):
    pugurl="https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/{}/XML".format(cas)
    try:
        page=requests.get(pugurl)
    except HTTPError as e:
        print('The server couldn\'t fulfill the request.')
        print('Error code: ', e.code)
    except URLError as e:
        print('We failed to reach a server.')
        print('Reason: ', e.reason)

    soup = BeautifulSoup(page.content,"xml")
    try:
        cid=soup.find("PC-CompoundType_id_cid").getText()
    except AttributeError as e:
        print("XML error", e , " with {}".format(pugurl))
        return(None)
    return("cid"+cid)


def get_summary(cas):
    cid=get_cid(cas)
    if cid is None:
        return({"B":1}) #bad xml
    print("trying cas {} cid {}".format(cas,cid))
    entry=table.get_item(Key={'SourceID':cid})
    if 'Item' in entry:
        if 'trialSummary' in entry['Item']['Data'][0]['Value']['Table']:
            trialSummary=entry['Item']['Data'][0]['Value']['Table']['trialSummary']
            ckeys=[]
            cvals=[]
            for f in trialSummary:
                ckeys+=[f.split(':')[0]]
                cvals+=[int(f.split(':')[1])]
            tdict=dict(zip(ckeys, cvals))
            #['1:2', '2:1', 'T:1']
        else:
            return({"M":1}) #missing trial summary
    else:
        return({"N":1}) #no data
    return(tdict)

def divideCells(mysummary):
    cells = dict(zip(masterCols,masterValues))
    for s in mysummary.keys():
        cells[s]=mysummary[s]
    #https://stackoverflow.com/questions/19798153/difference-between-map-applymap-and-apply-methods-in-pandas
    return(pd.Series(cells))

workbook=pd.ExcelFile("MCE-Clinical_Compound_Library.xlsx")
ci=workbook.parse('Compound Information')
ci['Trial_Summary'] = ci['CAS Number'].map(get_summary)
ci[masterCols]=ci['Trial_Summary'].apply(divideCells)
ci.to_excel("annotated_compound_library.xlsx")

