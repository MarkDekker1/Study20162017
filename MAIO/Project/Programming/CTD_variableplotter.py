# ------------------------------------------------------
# Getting amount of CTD and 
# ------------------------------------------------------

which_depth=10 #meters
directory_CTD = 'C:\Users\Mark\Documents\Studie\MAIO_zip\MAIO/CTD_1m/'
CTD_files = glob.glob(directory_CTD+'*')
which_CTD_vec=np.arange(0,63,1)
Depth_matrix=[]
Temp_matrix=[]
Time_matrix=[]
Hour_matrix=[]
Minute_matrix=[]
Second_matrix=[]
Lat_vec_c=[]
Lon_vec_c=[]

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

    data=ReadData(Parameter_initial,comparison=To_compare,initialvalue=0)
    data.GetCTDData()
        
# ------------------------------------------------------
# Save relevant data at every iteration
# ------------------------------------------------------
    
    for j in range(0,len(data.depth)):
        if data.depth[j]==which_depth:
            Temp_matrix.append(data.temp[j])
            Lon_vec_c.append(data.lon)
            Lat_vec_c.append(data.lat)
            Time_matrix.append(data.time[j])
            Hour_matrix.append(data.hour[j])
            Minute_matrix.append(data.minute[j])
            Second_matrix.append(data.second[j])
            #print(number)

#%%
# ------------------------------------------------------
# Get Bathymetry
# ------------------------------------------------------

data=ReadData(Parameter_initial,comparison=To_compare,initialvalue=0)
data.GetBathymetryData()
Lat_bath=data.Lat_bath
Lon_bath=data.Lon_bath
Depth=data.Depth

    
#%%
# ------------------------------------------------------
# Plot temperatures of CTD horizontally
# ------------------------------------------------------

from scipy.interpolate import griddata
from matplotlib.mlab import griddata
import matplotlib.colors as colors

plt.figure(figsize=(10,5))
plt.scatter(np.array(Hour_matrix)+np.array(Minute_matrix)/60.+np.array(Second_matrix)/60.,Temp_matrix)