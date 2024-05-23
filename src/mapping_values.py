import FluxTube as ft
import GEO as gg
import numpy as np
import pandas as pd
from tqdm import tqdm 
import xarray as xr 
import datetime as dt 
import os 

def closest_value(values_list, target):
    return min(values_list, key = lambda x: abs(x - target))

def fluxtube_coordinates(
        apex, 
        year = 2013, 
        site = 'saa', 
        points = 50
        ):
    
    apx = ft.Apex(apex)
    
    rlat = apx.apex_lat_base(base = 75)
       
    glon, glat = gg.split_meridian(
            rlat,
            year,
            points,
            site = site
            )
    
    mlats = np.linspace(-rlat, rlat, points)
    
    return glon, glat, mlats, apx


def interpolate_data(ds):
    
    ds['lon'] = ds['lon'] - 180
    
    new_lon = np.linspace(ds.lon[0], ds.lon[-1], 365)
    
    new_lat = np.linspace(ds.lat[0], ds.lat[-1], 180)
    new_alt = np.linspace(ds.lvl[0], ds.lvl[-1], 50)
    
    return ds.interp(
        lat = new_lat, lon = new_lon, lvl = new_alt)


def get_parameter_along_line(ds, apex, parameter = 'ti'):
    time =  ds.time.values
    
    ds['lon'] = ds['lon'] - 180
    
    new_lon = np.linspace(ds.lon[0], ds.lon[-1], 365)
    
    new_lat = np.linspace(ds.lat[0], ds.lat[-1], 180)
    new_alt = np.linspace(ds.lvl[0], ds.lvl[-1], 50)
    
    dsi = ds.interp(
        lat = new_lat, 
        lon = new_lon, 
        lvl = new_alt)

    out = {
        "glat": [], 
        "glon": [], 
        "alt":  [], 
        "mlat": [], 
        parameter: []
        }
    
    glon, glat, mlats, apx = fluxtube_coordinates(
        apex, site = 'saa', points = 50)
    
    for i in range(len(glon)):
        
        mlat = mlats[i]
        
        rlat = apx.apex_height(mlat) 
        
        target_lon = closest_value(new_lon, glon[i])
        
        target_lat = closest_value(new_lat, glat[i])
        
        target_alt = closest_value(new_alt, rlat)
        
        
        sel_vls = dsi.sel(
            lat = target_lat, 
            lon = target_lon, 
            lvl = target_alt
            )
        
        out['alt'].append(target_alt)
        out['glon'].append(target_lon)
        out['glat'].append(target_lat)
        out['mlat'].append(mlat)
        out[parameter].append(sel_vls[parameter].values)
        
    ds = pd.DataFrame(out)
    ds['apex'] = apex
    ds['time'] = time
    return ds


def get_in_time(ds, apex, parameter = 'ti'):
    
    out = []
    
    
    for time in ds['time'].values:
    
        out.append(get_parameter_along_line(
            ds.sel(time = time), apex, parameter))
        
    return pd.concat(out)


def load_dataset(infile):
    ds = xr.open_dataset(infile)
    
    ds = ds.where(ds['lvl'] < 320, drop=True)
    return ds

def get_parameter_name(file):
    
    f = file.split('.')[0]
    
    parameter = f[:-11]
    
    date_str = f.replace(parameter, '')[:-3]
    date = dt.datetime.strptime(date_str, '%Y%m%d')
    return parameter, date



def run_in_apex(
        infile,
        file,
        amin = 280, 
        amax = 320, 
        step = 10
        ):
    
    ds = load_dataset(infile + file)
    
    parameter, date = get_parameter_name(file)
    out = [] 
    heights = np.arange(amin, amax + step, step)
    for apex in tqdm(heights, parameter):
        out.append(get_in_time(ds, apex, parameter))
    
    df = pd.concat(out).set_index('time')
    return df 

infile = 'GAIA/data/netcdfs/'


def running(infile):
    
    
    for file in os.listdir(infile):
        
        
        df = run_in_apex(infile, file)
        
        file_to_save = file.replace('nc', '')
        
        df.to_csv('GAIA/data/fluxtube/' + file_to_save)
        
        
# running(infile)

file = 'te20130101cpl.nc'
df = run_in_apex(infile, file)

file_to_save = file.replace('nc', '')

df.to_csv('GAIA/data/fluxtube/' + file_to_save)
