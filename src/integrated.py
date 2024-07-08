# -*- coding: utf-8 -*-
"""
Created on Thu Jul  4 12:16:49 2024

@author: Luiz
"""

infile = 'test_gaia'

def test_gaia():
    df = pd.read_csv(infile, index_col = 0)
    
    out = []
                     
    for dn in tqdm(df.index.unique()):
            
        df1 = IntegratedParameters(df.loc[df.index == dn])
        
        df1['dn'] = dn
        out.append(df1)
        
    df = pd.concat(out)
    
    ds = df.loc[
        ((df.index == 300) & 
        (df['hem'] == 'south'))].set_index('dn')
    
    ds.index = pd.to_datetime(ds.index)


import datetime as dt 
import base as b 
infile = 'FluxTube/data/reduced/saa/2013.txt'

# df = pd.read_csv(infile, index_col=0)

df = b.load(infile)

ds = df.loc[df.index.date == dt.date(2013, 1, 1)]