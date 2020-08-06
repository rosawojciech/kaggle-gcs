last_update = '2020-08-06'
import csv
import os
import pkgutil
import sys
import re

d = os.path.join(os.path.dirname(sys.modules['kagglegcs'].__file__),'data')
D = {}
filename = os.listdir( d )[0]
# obtaining version
p = re.compile('[a-z_]+([0-9])_([0-9])_([0-9])')
matchObj = p.match(filename)
__version__ = matchObj.group(1) + '.' + matchObj.group(2)+'.' +  matchObj.group(3)

with open(os.path.join(d,filename), 'r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    for row in csv_reader:
        D[row["kaggle_dataset"]] = row['gcs_path'] 
        
Dl = [d for d in D]

def get_gcs_path(name):
    try:
        result = D[name]
    except KeyError: 
        print('Warning: no gcs_path found')
        result = ''
    return result

def gcs_info():
    print('Current kagglegcs version: '+__version__)
    print('Last datasets update: '+ last_update)
    print('Number of available datasets: '+str(len(Dl)))

def gcs_available(pattern = None):
    if pattern == None:
        return Dl 
    else:
        r = re.compile(pattern)
        return list(filter(r.match, Dl ))
