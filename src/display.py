import matplotlib.pyplot as plt
import cartopy.crs as ccrs

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