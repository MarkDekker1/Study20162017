# ------------------------------------------------------
# Defining station-couples
# ------------------------------------------------------

which_CTD_vec=[9,10,22,21,8,7,6,19,11,4,3,3,16,15,62,61,60,59,59,58,58,58,57,56,55,54,53]
which_SCAMP_vec=[22,23,33,32,21,29,18,30,25,17,16,15,29,28,13,12,11,10,9,8,7,6,5,4,3,2,1]

#which_CTD_vec=[which_CTD_vec[which]]
#which_SCAMP_vec=[which_SCAMP_vec[which]]
Error_matrix=[]
Depth_matrix=[]
Temp_matrix_s=[]
Temp_matrix_c=[]
Temp_matrix_sref=[]
Temp_matrix_dref=[]
Temp_matrix_cref=[]
Lat_vec=[]
Lon_vec=[]

# ------------------------------------------------------
# Start iteration
# ------------------------------------------------------
for couple in range(0,len(which_CTD_vec)):
    which_CTD=which_CTD_vec[couple]
    which_SCAMP=which_SCAMP_vec[couple]

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
    data_s=ReadData(Parameter_initial,comparison=To_compare,initialvalue=0)
    data_s.GetScampData()
    data_comp=ReadData(Parameter_initial,comparison=To_compare,initialvalue=0)
    data_comp.SegmentData(data_s.temp_acc,data_c.temp,data_s.depth,data_c.depth)

# ------------------------------------------------------
# Save data at every iteration
# ------------------------------------------------------

    
    if isnan(np.nanmean(data_comp.error))==False:
        Error_matrix.append(data_comp.error)
        Temp_matrix_s.append(data_comp.temp_s)
        Temp_matrix_sref.append(Compare(data_c.temp,data_s.temp_acc,data_c.depth,data_s.depth)[0])
        Temp_matrix_dref.append(Compare(data_c.temp,data_s.temp_acc,data_c.depth,data_s.depth)[1])
        Temp_matrix_cref.append(Compare(data_c.temp,data_s.temp_acc,data_c.depth,data_s.depth)[2])
        Temp_matrix_c.append(data_comp.temp_c)
        Depth_matrix.append(data_comp.depth)
        Lon_vec.append(data_c.lon)
        Lat_vec.append(data_c.lat)
    print(couple)
    
    
# ------------------------------------------------------
# Plot temperatures of CTD and SCAMP in scatterplot (colors=depth)
# ------------------------------------------------------
#%%
plt.figure(num=None, figsize=(8,4),dpi=150, facecolor='w', edgecolor='k')
cm = plt.cm.get_cmap('jet')
for i in range(0,len(Temp_matrix_s)):
    #colors=np.linspace(Depth_matrix[i][0],Depth_matrix[i][len(Depth_matrix[i])-1],len(Temp_matrix_s[i]))
    #sc=plt.scatter(Temp_matrix_s[i],Temp_matrix_c[i], c=colors,vmin=0,vmax=50, alpha=0.8,s=50,cmap=cm)
    colors=np.linspace(Temp_matrix_dref[i][0],Temp_matrix_dref[i][len(Temp_matrix_dref[i])-1],len(Temp_matrix_sref[i]))
    sc=plt.scatter(Temp_matrix_sref[i],Temp_matrix_cref[i], c=colors,vmin=0,vmax=50, alpha=0.8,s=50,cmap=cm,marker='D')

plt.colorbar(sc)
plt.plot([27,30], [27,30],'k')
plt.ylabel('Temperature CTD [K]',fontsize=15)
plt.xlabel('Temperature SCAMP [K]',fontsize=15)
plt.xlim([27,30])
plt.ylim([27,30])
plt.tick_params(axis='both', which='major', labelsize=15)

# ------------------------------------------------------
# Plot RSME versus maximum depth (colors=Latitude)
# ------------------------------------------------------
#%%
RSME_vec=[]
Depth_vec=[]
cm = plt.cm.get_cmap('jet')

for i in range(0,len(Temp_matrix_s)):
    RSME_vec.append(np.sqrt(np.mean((np.array(Temp_matrix_s[i])-np.array(Temp_matrix_c[i]))**2)))
    Depth_vec.append(np.max(Depth_matrix[i]))

colors=Lat_vec
plt.figure(num=None, figsize=(8,4),dpi=150, facecolor='w', edgecolor='k')
sc=plt.scatter(Depth_vec,RSME_vec, c=colors,alpha=0.5,s=150,cmap=cm,vmin=17.30,vmax=17.65)
plt.colorbar(sc)
plt.ylabel('RSME [K]',fontsize=15)
plt.xlabel('Depth [m]',fontsize=15)
plt.tick_params(axis='both', which='major', labelsize=15)

# ------------------------------------------------------
# Plot depth profiles: segmented
# ------------------------------------------------------
#%%
plt.figure(num=None, figsize=(8,4),dpi=150, facecolor='w', edgecolor='k')
plt.plot(Temp_matrix_s[0],Depth_matrix[0], 'r-',linewidth=2)
plt.plot(Temp_matrix_c[0],Depth_matrix[0],'k-',linewidth=2)
plt.ylabel('Depth [m]',fontsize=15)
plt.xlabel('Temperature [K]',fontsize=15)
plt.tick_params(axis='both', which='major', labelsize=15)
#plt.ylim([max(list(depth_c)+list(depth_s)) + 5, min(list(depth_c)+list(depth_s)) - 0.5])
plt.ylim([np.max(Depth_matrix[0])+5,0])
plt.legend(['SCAMP, down','SCAMP, up','CTD'],loc='best')


# ------------------------------------------------------
# Plot depth profiles: raw
# ------------------------------------------------------
#%%
plt.figure(num=None, figsize=(8,4),dpi=150, facecolor='w', edgecolor='k')
plt.plot(data_s.temp_acc[:data_s.down_cast],data_s.depth[:data_s.down_cast], 'r-',linewidth=2)
plt.plot(data_s.temp_acc[data_s.down_cast:data_s.surface],data_s.depth[data_s.down_cast:data_s.surface],'k-',linewidth=2)
plt.plot(data_c.temp,data_c.depth,'g-',linewidth=2)
plt.ylabel('Depth [m]',fontsize=15)
plt.xlabel('Temperature [K]',fontsize=15)
plt.tick_params(axis='both', which='major', labelsize=15)
plt.ylim([np.max(Depth_matrix[0])+5,0])
plt.legend(['SCAMP, down','SCAMP, up','CTD'],loc='best')