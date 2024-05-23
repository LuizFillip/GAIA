import pandas as pd
import os 
import aeronomy as ae

infile = 'GAIA/data/fluxtube/'


def join_parameters(infile):
    
    out = []
    for file in os.listdir(infile):
        
        out.append(pd.read_csv(infile + file, index_col = 0))
        
    df = pd.concat(out, axis = 1)
    
    df = df.loc[:,~df.columns.duplicated()].copy()
    
    df = df.rename(
        columns = {
            'ginao': 'O',
            'ginmo': 'O2',
            'ginmn': 'N2',
            'ginuu': 'zon',
            'ginvv': 'mer',
            'xoi': 'Oi',
            'xo2i': 'O2i',
            'xnoi': 'NOi',
            'xn2i': 'N2i',
            'te': 'Te',
            'gintmp': 'Tn'
            
            }
        
        )
    
    
    df['ne'] = df[['N2i', 'O2i', 'N2i', 'NOi']].sum(axis = 1)
    
    # df = df.drop(
    #     columns = ['N2i', 'O2i', 'N2i',]
    #     )
    return df


df = join_parameters(infile)

df = ae.magnetic_parameters(df)

df = ae.conductivity_parameters(df)
 
df = ae.winds_parameters(df)

#%%%
df.to_csv('test_gaia')

# df.columns 