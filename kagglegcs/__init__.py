import csv
import os
D = {}
workdir = './kagglegcs/'
filename = os.listdir( workdir )[0]
with open(workdir + filename, mode='r') as csv_file:
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
