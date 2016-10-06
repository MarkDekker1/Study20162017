# ------------------------------------------------------
# Getting amount of CTD and 
# ------------------------------------------------------

from scipy import interpolate
which_depth=10 #meters
Depth_matrix=[]
Temp_matrix=[]
Lat_vec_s=[]
Lon_vec_s=[]
Depth_vec=np.arange(0,50,1)

# ------------------------------------------------------
# Start iteration
# ------------------------------------------------------
for number in range(0,36):
    which_SCAMP=number
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
    
        
    
    print(number)

#%%
plt.figure(figsize=(10,10))
plt.scatter(Lon_vec_s,Lat_vec_s)
for i in range(0,36):
    plt.annotate(i,(Lon_vec_s[i],Lat_vec_s[i]),ha='center',va='top')