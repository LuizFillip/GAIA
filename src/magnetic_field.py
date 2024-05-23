import pyIGRF
import numpy as np
from tqdm import tqdm
import pandas as pd 
infile = 'GAIA/data/netcdfs/'

def run_igrf(sel_ds):
         
    out = {'F': [], 
           'D': [], 
           'I': [], 
           'lon': [], 
           'lat': [], 
           }
    for lat in tqdm(sel_ds['lat']):
        for lon in sel_ds['lon']:
            
            D, I, _, _, _, _, F = pyIGRF.igrf_value(
                lat, lon, 
                alt = 300, 
                year = 2013
                )
            
            for key in out.keys():
                
                out[key].append(vars()[key])
            
    df = pd.DataFrame(out)
    
    df.to_csv(infile + 'mag20130101cpl')