import xarray as xr 


infile = 'GAIA/data/'

file = 'ti20130101cpl.nc'


year = 2013
ds = xr.open_dataset(infile + file)

ds = ds.where(ds['lvl'] < 320, drop=True)


df = run_in_apex(ds)

