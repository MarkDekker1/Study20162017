# ------------------------------------------------------
# Getting amount of CTD and 
# ------------------------------------------------------

from scipy import interpolate
which_depth=10 #meters
#which_CTD_vec=np.arange(15,22+1,1)
#which_CTD_vec=[1,2,3,4,5,6,7,8]
which_CTD_vec=np.arange(53,60+1,1)
Depth_matrix=[]
Temp_matrix=[]
Lat_vec_c=[]
Lon_vec_c=[]
#Depth_vec=np.arange(0,50,1)
#Depth_vec=np.arange(0,50,1)
Depth_vec=np.arange(0,400,1)

# ------------------------------------------------------
# Start iteration
# ------------------------------------------------------
for number in range(0,len(which_CTD_vec)):
    which_CTD=which_CTD_vec[number]
    which_SCAMP=1

# ------------------------------------------------------
# Defining parameters
# ------------------------------------------------------
    
    Parameter_initial={
        'which_CTD':which_CTD,
        'which_SCAMP':which_SCAMP
        }
    To_compare='temp'

# ------------------------------------------------------
# Get data
# ------------------------------------------------------

    data_c=ReadData(Parameter_initial,comparison=To_compare,initialvalue=0)
    data_c.GetCTDData()
    
# ------------------------------------------------------
# Save relevant data at every iteration
# ------------------------------------------------------
    
    Lon_vec_c.append(data_c.lon)
    Lat_vec_c.append(data_c.lat)
    
    
    z = data_c.depth
    T = data_c.temp
    f = interpolate.interp1d(z,T)    
    
    zmin = np.int(np.min(z))
    zmax = np.int(np.max(z))
    
    znew=np.zeros(len(Depth_vec))
    for i in range(0,len(Depth_vec)):
        if i<zmin:
            znew[i]='nan'
        if i>=zmin and i<zmax:
            znew[i]=f(Depth_vec[zmin:zmax])[i-zmin]
        if i>=zmax:
            znew[i]='nan'
    
    Temp_matrix.append(znew)
    Depth_matrix.append(Depth_vec[zmin:zmax])
    
    
    print(number)

#%%
# ------------------------------------------------------
# Process stations CTD
# ------------------------------------------------------

Station_vec=which_CTD_vec

# ------------------------------------------------------
# Get Bathymetry at locations
# ------------------------------------------------------

data=ReadData(Parameter_initial,comparison=To_compare,initialvalue=0)
data.GetBathymetryData()
Lat_bath=data.Lat_bath
Lon_bath=data.Lon_bath
Depth=data.Depth

Bath=[]
Distance=0.005
commons_lon=[]
for i in range(0,len(Lon_vec_c)):
    more=where(Lon_bath>=Lon_vec_c[i]-Distance)
    less=where(Lon_bath<=Lon_vec_c[i]+Distance)
    commons_lon.append(np.intersect1d(more,less)[0])
    
commons_lat=[]
for j in range(0,len(Lat_vec_c)):
    more=where(Lat_bath>=Lat_vec_c[j]-Distance)
    less=where(Lat_bath<=Lat_vec_c[j]+Distance)
    commons_lat.append(np.intersect1d(more,less)[0])

stations_depth=[]
for i in range(0,len(Lat_vec_c)):
    stations_depth.append(Depth[commons_lat[i],commons_lon[i]])

#vmin=27
#for i in range(0,len(Temp_matrix)):
#    for j in range(0,len(Temp_matrix)):
#        if Temp_matrix[i][j]<vmin:
#            Temp_matrix[i][j]='nan'
    
# ------------------------------------------------------
# Plot temperatures of CTD vertically
# ------------------------------------------------------
    
from scipy.interpolate import griddata
from mpl_toolkits.basemap import Basemap
from matplotlib.mlab import griddata
import matplotlib.colors as colors

plt.figure(figsize=(10,5))
c=plt.contourf(Station_vec,-Depth_vec[2:],np.transpose(Temp_matrix)[2:],100)
c2=plt.contour(Station_vec,-Depth_vec[2:],np.transpose(Temp_matrix)[2:],25,zorder=15,colors='k')
plt.plot(Station_vec,stations_depth,'k',linewidth=2,zorder=50)
plt.fill_between(Station_vec, -10000, stations_depth, facecolor='saddlebrown',zorder=50)
plt.ylim([-np.max(Depth_vec),-2])
plt.colorbar(c)
#plt.clim([27,30])
plt.ylabel('Depth [m]',fontsize=15)
plt.xlabel('Station Number',fontsize=15)
plt.tick_params(axis='both', which='major', labelsize=15)
plt.legend(['Bottom'],loc='lower left')