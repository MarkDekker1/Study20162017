# ------------------------------------------------------
# Choosing depth
# ------------------------------------------------------

which_depth_max=15 #meters
which_depth_min=1 #meters
which_variable='dissipation'

# ------------------------------------------------------
# Define path and gaining special variable
# ------------------------------------------------------

directory = 'C:\Users\Mark\Documents\Studie\MAIO_Project\Data'
file = open(directory+ '/'+ which_variable+'.txt', 'r')
lines = file.readlines()
file.close()
variable_vec=[]
for line_i in range(1,len(lines)):
    line = lines[line_i].split()
    
    variable_vec.append(line[np.int(which_depth_min*2+1):np.int(which_depth_max*2+1)])

variable=[]
for i in range(0,len(variable_vec)):
    dummy=[]
    for j in range(0,len(variable_vec[i])):
        dummy.append(np.float(variable_vec[i][j]))
    variable.append(np.nanmean(dummy))

# ------------------------------------------------------
# Gain locations of SCAMP stations
# ------------------------------------------------------

Parameter_initial={
    'which_CTD':1,
    'which_SCAMP':1
    }
To_compare='temp'

data_loc=ReadData(Parameter_initial,comparison=To_compare,initialvalue=0)
data_loc.GetStationLocations()
Lat_vec=data_loc.lat_s
Lon_vec=data_loc.lon_s
        
#%%
# ------------------------------------------------------
# Plot special quantity horizontally
# ------------------------------------------------------

from scipy.interpolate import griddata
from mpl_toolkits.basemap import Basemap
from matplotlib.mlab import griddata
import matplotlib.tri as mtri
from matplotlib.tri import Triangulation, TriAnalyzer, UniformTriRefiner
import matplotlib.mlab as mlab

plt.figure(figsize=(10,10))
m = Basemap(projection = 'merc',
llcrnrlat=17, urcrnrlat=18.1,
llcrnrlon=-64.5, urcrnrlon=-60.3,
resolution='i', area_thresh=0.001)

xi = np.linspace(np.min(Lon_vec),np.max(Lon_vec), 100)
yi = np.linspace(np.min(Lat_vec),np.max(Lat_vec),100)
points = np.transpose([Lon_vec,Lat_vec])
zi = griddata(Lon_vec,Lat_vec, variable, xi, yi, interp='linear')
        
x,y=m(xi,yi)
colors=plt.contourf(x,y,zi,25,cmap=plt.cm.jet)

lon,lat=m(Lon_vec,Lat_vec)
m.scatter(lon,lat,s=40,alpha=0.7,c='k',marker=(5, 2))
cbar = m.colorbar(colors, extend='both', location='bottom',pad="10%")

m.drawcoastlines(linewidth=0.2)
m.drawcountries()
m.drawmapboundary()
m.fillcontinents(color='#cc9966')#,lake_color='#99ffff')
par = m.drawparallels(np.arange(15,20,0.5),labels=[1,0,0,0])
mer = m.drawmeridians(np.arange(-65,-59,1),labels=[0,0,0,1])