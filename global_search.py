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
from boto3.dynamodb.conditions import Key, Attr

masterCols=['B','N','1','2','3','4','M','R','T','W','?']
masterValues=[0,0,0,0,0,0,0,0,0,0,0]

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('pubchem_ct_annos')

response = table.scan()

for i in response['Items']:
    print(i['Data'][0]['Value']['Table'])
