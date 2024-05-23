import xarray as xr 

infile = 'GAIA/data/netcdfs/'

file_paths = [
    'xo2i20130101cpl.nc', 
    'xoi20130101cpl.nc',
    'xnoi20130101cpl.nc', 
    'xn2i20130101cpl.nc'
    ]


def concataned_datasets(
        file_paths
        ):
    datasets = [xr.open_dataset(infile + fp) for fp in file_paths]
    
    ds = xr.merge(datasets)
    
    sum_variable = xr.zeros_like(next(iter(ds.data_vars.values())))
    
    # Sum all variables in the dataset
    for var in ds.data_vars:
        sum_variable += ds[var]
    
    # Add the new variable to the dataset
    ds['ne'] = sum_variable


    ds['lon'] = ds['lon'] - 180
    
    return ds 


# ds.loc[ds['lon'] == -45]


# ds1 = ds.where(ds['lvl'] < 1000, drop=True)


# ds1 = ds1.isel(time = 0)

# ds1.sel(lon = -45, lat = 0)['ne'].plot(y = 'lvl')