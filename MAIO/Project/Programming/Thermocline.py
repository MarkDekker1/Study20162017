# ------------------------------------------------------
# Defining station-couples
# ------------------------------------------------------

CTD_files = glob.glob(directory_CTD+'*')
which_CTD_vec=np.arange(0,len(CTD_files),1)
Depth_matrix=[]
Temp_matrix_c=[]
Lat_vec=[]
Lon_vec=[]

# ------------------------------------------------------
# Start iteration
# ------------------------------------------------------
for CTD_number in range(0,len(which_CTD_vec)):
    which_CTD=which_CTD_vec[CTD_number]
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
    
    Temp_matrix_c.append(data_c.temp)
    Depth_matrix.append(data_c.depth)
    Lon_vec.append(data_c.lon)
    Lat_vec.append(data_c.lat)
    
    print(CTD_number)
    
#%%
# ------------------------------------------------------
# Plot temperatures of CTD versus depth in scatterplot
# ------------------------------------------------------
    
plt.figure(num=None, figsize=(8,4),dpi=150, facecolor='w', edgecolor='k')
for i in range(0,len(Temp_matrix_c)):
    plt.plot(Temp_matrix_c[i],Depth_matrix[i],'k-',linewidth=2)
plt.xlabel(r'Temperature CTD [$^o$C]',fontsize=15)
plt.ylabel('Depth [m]',fontsize=15)
plt.ylim([5000,0])
plt.tick_params(axis='both', which='major', labelsize=15)

#%%
# ------------------------------------------------------
# Plot temperature gradient of CTD versus depth in scatter plot
# ------------------------------------------------------

smoothening=5 #in meters
div=np.int(smoothening/2)
thermocline=[]
thermothresh=-0.1

plt.figure(num=None, figsize=(8,4),dpi=150, facecolor='w', edgecolor='k')
for i in range(0,len(Temp_matrix_c)):
    Tempgrad=[]
    Tempgraddepth=[]
    for j in range(div,len(Temp_matrix_c[i])-div):
        Tempgrad.append((Temp_matrix_c[i][j+div]-Temp_matrix_c[i][j-div])/smoothening)
        Tempgraddepth.append(Depth_matrix[i][j])
    if len(np.where(np.array(Tempgrad) <=thermothresh)[0])!=0:
        thermocline.append(Tempgraddepth[np.where(np.array(Tempgrad) <=thermothresh)[0][0]])
    else:
        thermocline.append(-20)
    
plt.hist(thermocline,25, alpha=0.75)
plt.xlim([0,200])
plt.ylabel(r'Frequency Thermocline',fontsize=15)
plt.xlabel('Depth [m]',fontsize=15)
plt.tick_params(axis='both', which='major', labelsize=15)
