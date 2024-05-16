import FluxTube as ft
import xarray as xr 
import GEO as gg
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import pandas as pd
from tqdm import tqdm 


def plot_map(dsi, glon, glat):
    

    fig, ax = plt.subplots(
          figsize = (10, 10), 
          ncols = 1,
          dpi = 300, 
          subplot_kw = 
          {'projection': ccrs.PlateCarree()}
          )
    
    gg.map_attrs(
        ax, 
        year, 
        grid = False,
        degress = None
        )
    
    ax.contourf(dsi['lon'], dsi['lat'], dsi['ti'], 30, cmap = 'jet')
    
    ax.plot(glon, glat, lw = 2)


def closest_value(values_list, target):
    return min(values_list, key = lambda x: abs(x - target))



def fluxtube_coordinates(apex, year = 2013, site = 'saa', points = 50):
    
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
    
    return ds.interp(lat = new_lat, lon = new_lon, lvl = new_alt)


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
    
    
    for time in tqdm(ds['time'].values, str(apex)):
    
        out.append(get_parameter_along_line(
            ds.sel(time = time), apex, parameter))
        
    return pd.concat(out)

def run_in_apex(
        ds,
        parameter = 'ti',
        amin = 280, 
        amax = 320, 
        step = 10
        ):
    
    out = [] 
    
    for apex in np.arange(amin, amax + step, step):
        out.append(get_in_time(ds, apex, parameter))
    
    
    return pd.concat(out)



infile = 'GAIA/data/'

file = 'ti20130101cpl.nc'


year = 2013
ds = xr.open_dataset(infile + file)

ds = ds.where(ds['lvl'] < 320, drop=True)


df = run_in_apex(ds)

