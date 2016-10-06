# ------------------------------------------------------
# Preambule
# ------------------------------------------------------ 
   
from netCDF4 import Dataset
from mpl_toolkits.basemap import Basemap
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors

# ------------------------------------------------------
# Read Data Bathymetry (BODC)
# ------------------------------------------------------    

file = 'C:\Users\Mark\Documents\Studie\MAIO_Project\Data\GEBCO_2014_2D_-100.0_0.0_-50.0_40.0.nc'
ncdf = Dataset(file, mode='r')
Lat = ncdf.variables['lat'][:]
Lon = ncdf.variables['lon'][:]
Depth = ncdf.variables['elevation'][:]
Depth = Depth[2000:2565,4200:4765]
Lon_bath = Lon[4200:4765]
Lat_bath = Lat[2000:2565]
for i in range(0,len(Depth)):
    for j in range(0,len(Depth[0])):
        if Depth[i][j]>=0:
            Depth[i][j]=-0.1

#%%
# ------------------------------------------------------
# Plot
# ------------------------------------------------------    

plt.figure(figsize=(15,15))
m = Basemap(projection = 'merc',
llcrnrlat=17, urcrnrlat=18.1,
llcrnrlon=-64.5, urcrnrlon=-60.3,
resolution='i', area_thresh=0.001)

x,y=m(Lon_bath,Lat_bath)
c=plt.contourf(x,y,-Depth,cmap=plt.cm.BrBG,levels=[10,15,20,25,50,100,250,500,750,1000,2000,3000,4000,5000,6000,7000],norm=colors.LogNorm(vmin=10,vmax=5000))

cbar = m.colorbar(c,ticks=[1e1,1e2,1e3,1e4], extend='both', location='bottom',pad="10%")#spacing='uniform'

m.drawcoastlines(linewidth=0.2)
m.drawcountries()
m.drawmapboundary()
m.fillcontinents(color='#cc9966')
par = m.drawparallels(np.arange(15,20,0.5),labels=[1,0,0,0])
mer = m.drawmeridians(np.arange(-65,-59,1),labels=[0,0,0,1])