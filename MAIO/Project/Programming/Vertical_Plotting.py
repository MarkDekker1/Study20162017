# ------------------------------------------------------
# Getting amount of CTD and 
# ------------------------------------------------------

from scipy import interpolate
which_depth=10 #meters
which_SCAMP_vec=np.arange(27,33,1)
Depth_matrix=[]
Temp_matrix=[]
Lat_vec_s=[]
Lon_vec_s=[]
Depth_vec=np.arange(0,50,1)

# ------------------------------------------------------
# Start iteration
# ------------------------------------------------------
for number in range(0,len(which_SCAMP_vec)):
    which_SCAMP=which_SCAMP_vec[number]
    which_CTD=1

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

    data_s=ReadData(Parameter_initial,comparison=To_compare,initialvalue=0)
    data_s.GetScampData()
    
# ------------------------------------------------------
# Save relevant data at every iteration
# ------------------------------------------------------
    
    Lon_vec_s.append(data_s.lon)
    Lat_vec_s.append(data_s.lat)
    
    
    z = data_s.depth
    T = data_s.temp_acc
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
# Process double measurements at one location in case 11-16
# ------------------------------------------------------

#We know that 1,2 and 5,6 are at the same location: take nanmean
Temp_matrix2=[]
for i in range(0,len(which_SCAMP_vec)):
    matrix=[]
    if i==1:
        for j in range(0,len(Temp_matrix[1])):
            matrix.append(np.nanmean([Temp_matrix[1][j],Temp_matrix[2][j]]))
        Temp_matrix2.append(matrix)
    if i==0 or i==3 or i==4 or i==7:
        matrix=Temp_matrix[i]
        Temp_matrix2.append(matrix)
    if i==5:
        for j in range(0,len(Temp_matrix[5])):
            matrix.append(np.nanmean([Temp_matrix[5][j],Temp_matrix[6][j]]))
        Temp_matrix2.append(matrix)
        
Station_vec=[11,12,12.5,13,14,15,15.5,16]

#%%
# ------------------------------------------------------
# Process double measurements at one location in case 21-25
# ------------------------------------------------------

#We know that 2,3 are at the same location: take nanmean
Temp_matrix2=[]
for i in range(0,len(which_SCAMP_vec)):
    matrix=[]
    if i==3:
        for j in range(0,len(Temp_matrix[1])):
            matrix.append(np.nanmean([Temp_matrix[2][j],Temp_matrix[3][j]]))
        Temp_matrix2.append(matrix)
    if i==0 or i==1 or i==4 or i==5:
        matrix=Temp_matrix[i]
        Temp_matrix2.append(matrix)
        
Station_vec=[21,22,23,23.5,24,25]

#%%
# ------------------------------------------------------
# Get Bathymetry at locations
# ------------------------------------------------------

data=ReadData(Parameter_initial,comparison=To_compare,initialvalue=0)
data.GetBathymetryData()
Lat_bath=data.Lat_bath
Lon_bath=data.Lon_bath
Depth=data.Depth

#%%
Bath=[]
Distance=0.005
commons_lon=[]
for i in range(0,len(Lon_vec_s)):
    more=where(Lon_bath>=Lon_vec_s[i]-Distance)
    less=where(Lon_bath<=Lon_vec_s[i]+Distance)
    commons_lon.append(np.intersect1d(more,less)[0])
    
commons_lat=[]
for j in range(0,len(Lat_vec_s)):
    more=where(Lat_bath>=Lat_vec_s[j]-Distance)
    less=where(Lat_bath<=Lat_vec_s[j]+Distance)
    commons_lat.append(np.intersect1d(more,less)[0])

stations_depth=[]
for i in range(0,len(Lat_vec_s)):
    stations_depth.append(Depth[commons_lat[i],commons_lon[i]])

stations_unique=[]    
for i in range(0,6):
    if i!=3:
        stations_unique.append(stations_depth[i])
    
#%%
# ------------------------------------------------------
# Plot temperatures of CTD vertically
# ------------------------------------------------------
    
from scipy.interpolate import griddata
from mpl_toolkits.basemap import Basemap
from matplotlib.mlab import griddata
import matplotlib.colors as colors

plt.figure(figsize=(10,5))
c=plt.contourf(Station_vec,-Depth_vec[2:],np.transpose(Temp_matrix)[2:],100)
plt.plot(np.arange(21,26,1),stations_unique)
plt.ylim([-50,-2])
plt.colorbar(c)
plt.ylabel('Depth [m]',fontsize=15)
plt.xlabel('Station Number',fontsize=15)
plt.tick_params(axis='both', which='major', labelsize=15)
plt.legend(['Depth'],loc='lower left')