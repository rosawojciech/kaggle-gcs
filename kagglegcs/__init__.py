last_update = '2020-08-06'
import csv
import os
import pkgutil
import sys
import re
import tempfile
import time
from subprocess import Popen, PIPE


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

class kaggle_gcs_client:
    def __init__(self, command = 'kaggle'):
        self.command = command
        # user name
        process = Popen([self.command,"config","view"], stdout=PIPE, stderr=PIPE)
        stdout, stderr = process.communicate()
        p = re.compile("username: ([a-z0-9]+)")
        matchObj = p.search(stdout.decode('ascii'))
        self.username = matchObj.group(1)
        # user dictionary
        self.D = {}
        # one string passed
    def cache_gcs_paths(self, dsname):
        if isinstance(dsname, str):
            dsname = [dsname]
        with tempfile.TemporaryDirectory() as tmpdirname:
            
            #prepare cache-kaggle-gcs kernel
            kernel = create_kernel(dsname)
            f= open(os.path.join(tmpdirname,"kernel.py"),"w+t")
            f.write(kernel)
            f.close()
            #prepare cache-kaggle-gcs metadata
            metadata = create_metadata(self.username,dsname)
            f= open(os.path.join(tmpdirname,"kernel-metadata.json"),"w+t")
            f.write(metadata)
            f.close()
            
            #diagnosis
            #f = open(os.path.join(tmpdirname,"kernel-metadata.json"),"r+t")
            #print(f.read())
            #f.close()
            
            process = Popen([self.command,"kernels","push","-p",tmpdirname], stdout=PIPE, stderr=PIPE)
            stdout, stderr = process.communicate()
       
        with tempfile.TemporaryDirectory() as tmpdirname: 
            # wait for kaggle notebook completion
            time.sleep(5)
            matchObj = None
            tt = 0
            timeout = 120
            while matchObj is None and tt<timeout:
                tt +=1
                time.sleep(1)
                process = Popen([self.command,"kernels","status","cache-kaggle-gcs"], stdout=PIPE, stderr=PIPE)
                stdout, stderr = process.communicate()
                p = re.compile("complete")
                matchObj = p.search(stdout.decode('ascii'))
            # download results    
            process = Popen([self.command,"kernels","output",self.username+"/cache-kaggle-gcs","-p",tmpdirname], stdout=PIPE, stderr=PIPE)
            stdout, stderr = process.communicate()
            #print(stdout)
            #print(stderr)
            #print(os.listdir(tmpdirname))
            with open(os.path.join(tmpdirname,"cache_kaggle_gcs_paths.csv"), 'r') as csv_file:
                csv_reader = csv.DictReader(csv_file)
                for row in csv_reader:
                    self.D[row["kaggle_dataset_names"]] = row['gcs_path'] 
                    #print(row['gcs_path'])
        return self.D[dsname[0]]
    def get_gcs_path(self,dsname):
        try:
            return self.D[dsname]
        except KeyError:
            return self.cache_gcs_paths(dsname)
def create_kernel(x):
    
    cm = "import pandas as pd, numpy as np\n"
    cm += "from kaggle_datasets import KaggleDatasets\n"
    cm +="from datetime import datetime\n"
    cm += "now = datetime.now()\n"
    cm += "kaggle_dataset_names = ['"+ "','".join(x)+"']\n"
    cm += "kaggle_datasets =  [ft.split('/')[1] for ft in kaggle_dataset_names]\n"
    cm += "gcs_paths = []\n"
    cm += "for fi in kaggle_datasets:\n"
    cm += "\ttry:\n"
    cm += "\t\tgcs_paths.append(KaggleDatasets().get_gcs_path(fi))\n"
    cm += "\texcept:\n"
    cm += "\t\tgcs_paths.append('httpError')\n"
    cm += "result = pd.DataFrame({'kaggle_dataset_names': kaggle_dataset_names, 'gcs_path': gcs_paths})\n"
    #cm += "result.to_csv('cache_kaggle_gcs_paths_'+now.strftime('%d_%m_%Y_%H_%M_%S')+'.csv', index = False)"
    cm += "result.to_csv('cache_kaggle_gcs_paths.csv', index = False)"
    return cm
def create_metadata(username,x):
    mt = '{\n'
    mt += '"id": "'+username+'/cache-kaggle-gcs",\n'
    mt += '"title": "cache-kaggle-gcs",\n'
    mt += '"code_file": "kernel.py",\n'
    mt += '"language": "python",\n'
    mt += '"kernel_type": "script",\n'
    mt += '"is_private": "true",\n'
    mt += '"enable_gpu": "false",\n'
    mt += '"enable_internet": "true",\n'
    mt += '"dataset_sources": ["'+ '","'.join(x)+'"],\n'
    mt += '"competition_sources": [],\n'
    mt += '"kernel_sources": []}'
    return mt
    
#    write(metadata,file = "kernel/kernel-metadata.json",append = F)
#  }
