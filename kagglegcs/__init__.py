import csv
import os
import pkgutil
import sys
d = os.path.dirname(sys.modules['kagglegcs'].__file__)
D = {}

with open(os.path.join(d, '/kagglegcs/kaggle_gcs_paths_0_0_1.csv'), 'r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    for row in csv_reader:
        D[row["kaggle_dataset"]] = row['gcs_path'] 

def get_gcs_path(name):
    try:
        result = D[name]
    except KeyError: 
        print('Warning: no gcs_path found')
        result = ''
    return result
