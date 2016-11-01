# ------------------------------------------------------
# Defining station-couples
# ------------------------------------------------------

#which=17
#which_CTD_vec=[9,10,22,21,8,7,6,18,11,4,3,3,16,15,62,61,60,59,59,58,58,58,57,56,55,54,53,7]
#which_SCAMP_vec=[22,23,33,32,21,19,18,30,25,17,16,15,29,28,13,12,11,10,9,8,7,6,5,4,3,2,1,20]

which_SCAMP_vec=np.arange(0,35,1)
which_CTD_vec=[52,53,54,55,56,57,57,57,58,58,59,61,61,0,2,2,3,5,6,7,7,8,9,10,11,12,13,14,15,18,18,20,21,22,22]

which_CTD_vec=np.arange(1,63,1)
which_SCAMP_vec=np.zeros(63)+np.int(1)
#which_CTD_vec=[which_CTD_vec[which]]
#which_SCAMP_vec=[which_SCAMP_vec[which]]
Error_matrix=[]
Depth_matrix=[]
Temp_matrix_s=[]
Temp_matrix_c=[]
Temp_matrix_sref=[]
Temp_matrix_dref=[]
Temp_matrix_cref=[]
Lat_vec_c=[]
Lon_vec_c=[]
Lat_vec_s=[]
Lon_vec_s=[]
Bias_vector=[]
Lag_vector=[]
Timedif_vector=[]
ctd_time=[]
scamp_time=[]

# ------------------------------------------------------
# Start iteration
# ------------------------------------------------------

for couple in range(0,len(which_CTD_vec)):
    which_CTD=which_CTD_vec[couple]
    which_SCAMP=1#np.int(which_SCAMP_vec[couple])

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
        Lon_vec_c.append(data_c.lon)
        Lat_vec_c.append(data_c.lat)
        Lon_vec_s.append(data_s.lon)
        Lat_vec_s.append(data_s.lat)
        Bias_vector.append(Compare(data_c.temp,data_s.temp_acc,data_c.depth,data_s.depth)[3])
        Lag_vector.append(Compare(data_c.temp,data_s.temp_acc,data_c.depth,data_s.depth)[4])
        ctd_time.append(data_c.hour[0]+data_c.minute[0]/60.+data_c.second[0]/60.)
        scamp_time.append(data_s.time_fraction)
    print(couple)

    
# ------------------------------------------------------
# Plot temperatures of CTD and SCAMP in scatterplot (colors=depth)
# ------------------------------------------------------
#%%
plt.figure(num=None, figsize=(8,4),dpi=1000, facecolor='w', edgecolor='k')
cm = plt.cm.get_cmap('jet')
for i in range(0,len(Temp_matrix_s)):
    colors=np.linspace(Depth_matrix[i][0],Depth_matrix[i][len(Depth_matrix[i])-1],len(Temp_matrix_s[i]))
    sc=plt.scatter(Temp_matrix_s[i],Temp_matrix_c[i], c=colors,vmin=0,vmax=50, alpha=0.6,s=75,cmap=cm)
    #colors=np.linspace(Temp_matrix_dref[i][0],Temp_matrix_dref[i][len(Temp_matrix_dref[i])-1],len(Temp_matrix_sref[i]))
    #sc=plt.scatter(Temp_matrix_sref[i],Temp_matrix_cref[i], c=colors,vmin=0,vmax=50, alpha=0.6,s=75,cmap=cm)

a=plt.colorbar(sc)
plt.plot([27,30], [27,30],'k')
plt.ylabel(r'Temperature CTD [$^0 C$]',fontsize=15)
plt.xlabel(r'Temperature SCAMP [$^0 C$]',fontsize=15)
plt.xlim([27,30])
plt.ylim([27,30])
plt.tick_params(axis='both', which='major', labelsize=15)
a.ax.tick_params(labelsize=15)
a.set_label(r'Depth (m)',size=15)

savefig('Scatter_Raw.pdf',bbox_inches='tight')

# ------------------------------------------------------
# Plot depth profiles: raw
# ------------------------------------------------------
#%%
from scipy.stats import norm
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt

Error_matrix2=[]
for i in range(0,len(Temp_matrix_s)):
    Error_matrix2.append(np.array(Temp_matrix_sref[i])-np.array(Temp_matrix_cref[i]))

Error_matrix3=[]
maxdepth=300000
mindepth=30

for i in range(0,len(Error_matrix)):
    finder1=np.where(np.array(Depth_matrix[i])<maxdepth)[0]
    finder2=np.where(np.array(Depth_matrix[i])>mindepth)[0]
    finder = list(set(finder1).intersection(finder2))
    Error_vec=[]
    for j in finder:
        Error_vec.append(np.array(Error_matrix)[i][j])
    Error_matrix3.append(Error_vec)

CHOOSE=Error_matrix
#Error_matrix   : Raw
#Error_matrix2  : Refined with lag/bias
#Error_matrix3  : Specific depths

plt.figure(figsize=(8,4),dpi=1000)
matrix=[]
for i in range(0,len(CHOOSE)):
    matrix=matrix+list(CHOOSE[i])

matrix2=[]
for i in range(0,len(matrix)):
    if not isnan(matrix[i]):
        matrix2.append(matrix[i])
        
(mu, sigma) = norm.fit(matrix2)
n, bins, patches = plt.hist(matrix2, 60, normed=1, alpha=1,histtype='stepfilled')
y = mlab.normpdf( bins, mu, sigma)
l = plt.plot(bins, y, 'k--', linewidth=3)
#plt.plot([0,0], [0,max(y)],'-',color='k',linewidth=4,zorder=15)
#plt.plot([mu,mu], [0,max(y)],color='brown',linewidth=4,zorder=15)
#plt.plot([0,0], [0,10],'--',color='k',linewidth=2,zorder=1)
#plt.plot([mu,mu], [0,10],'--',color='brown',linewidth=2,zorder=1)
plt.plot([0,0], [0,10],'-',color='k',linewidth=3,zorder=1)
#plt.plot([mu,mu], [0,10],'-',color='r',linewidth=3,zorder=1)
plt.text(-0.75,8,'Mean',fontsize=15)
plt.text(-0.75,7,'Variance',fontsize=15)
#plt.text(-0.44,8,'-',fontsize=20)
plt.text(-0.4,8,round(mu,3),fontsize=15)
plt.text(-0.4,7,round(sigma**2.,3),fontsize=15)

plt.xlabel(r'Temperature error [$^0$C]',fontsize=15)
plt.xlim([-1,1])
plt.ylim([0,10])
plt.ylabel('Frequency',fontsize=15)
plt.tick_params(axis='both', which='major', labelsize=15)

#savefig('PDF_Calibrated.pdf',bbox_inches='tight')

# ------------------------------------------------------
# Plot depth profiles: Bias
# ------------------------------------------------------
#%%
plt.figure(figsize=(8,4),dpi=1000)
matrix=Bias_vector

matrix2=[]
for i in range(0,len(matrix)):
    if not isnan(matrix[i]):
        matrix2.append(matrix[i])
        
(mu, sigma) = norm.fit(matrix2)
n, bins, patches = plt.hist(matrix2, 15, normed=1, alpha=1,histtype='stepfilled')
y = mlab.normpdf( bins, mu, sigma)
l = plt.plot(bins, y, 'k--', linewidth=3)
plt.plot([0,0], [0,10],'-',color='k',linewidth=3,zorder=1)
#plt.plot([mu,mu], [0,10],'-',color='r',linewidth=3,zorder=1)
plt.text(-0.18,8,'Mean',fontsize=15)
plt.text(-0.18,7,'Variance',fontsize=15)
#plt.text(-0.44,8,'-',fontsize=20)
plt.text(-0.1,8,round(mu,3),fontsize=15)
plt.text(-0.1,7,round(sigma**2.,3),fontsize=15)

plt.xlabel(r'Temperature error [$^0$C]',fontsize=15)
#plt.xlim([-1,1])
plt.ylim([0,10])
plt.ylabel('Frequency',fontsize=15)
plt.tick_params(axis='both', which='major', labelsize=15)

savefig('PDF_Bias.pdf',bbox_inches='tight')

# ------------------------------------------------------
# Plot depth profiles: Lag
# ------------------------------------------------------
#%%
plt.figure(figsize=(8,4),dpi=1000)
matrix=Lag_vector

matrix2=[]
for i in range(0,len(matrix)):
    if not isnan(matrix[i]):
        matrix2.append(matrix[i])
        
(mu, sigma) = norm.fit(matrix2)
n, bins, patches = plt.hist(matrix2, 30, normed=1, alpha=1,histtype='stepfilled')
y = mlab.normpdf( bins, mu, sigma)
l = plt.plot(bins, y, 'k--', linewidth=3)
plt.plot([0,0], [0,10],'-',color='k',linewidth=3,zorder=1)
#plt.plot([mu,mu], [0,10],'-',color='r',linewidth=3,zorder=1)
#plt.text(-0.18,8,'Mean',fontsize=15)
#plt.text(-0.18,7,'Variance',fontsize=15)
#plt.text(-0.1,8,round(mu,3),fontsize=15)
#plt.text(-0.1,7,round(sigma**2.,3),fontsize=15)

plt.xlabel(r'Temperature error [$^0$C]',fontsize=15)
#plt.xlim([-1,1])
#plt.ylim([0,10])
plt.ylabel('Frequency',fontsize=15)
plt.tick_params(axis='both', which='major', labelsize=15)

#savefig('PDF_Bias.pdf',bbox_inches='tight')

# ------------------------------------------------------
# Plot RSME versus time difference
# ------------------------------------------------------
#%%
Timedif_vector=np.array(scamp_time)+3-np.array(ctd_time)
RSME_vec=[]
Depth_vec=[]
cm = plt.cm.get_cmap('jet')

for i in range(0,len(Temp_matrix_s)):
    RSME_vec.append(np.sqrt(np.mean((np.array(Temp_matrix_s[i])-np.array(Temp_matrix_c[i]))**2)))
    Depth_vec.append(np.max(Depth_matrix[i]))

colors=Depth_vec
plt.figure(num=None, figsize=(8,4),dpi=1000, facecolor='w', edgecolor='k')
sc=plt.scatter(np.abs(Timedif_vector),RSME_vec, c=colors,alpha=0.75,s=150,cmap=cm,edgecolor='k',linewidth=1.5)
a=plt.colorbar(sc)
plt.ylabel(r'RSME [$^0$C]',fontsize=15)
plt.xlabel('Absolute time difference [h]',fontsize=15)
plt.xlim([0,5.2])
plt.ylim([0,0.4])
plt.tick_params(axis='both', which='major', labelsize=15)
a.ax.tick_params(labelsize=15)
a.set_label(r'Depth (m)',size=15)

savefig('Timedifference.pdf',bbox_inches='tight')
#%%
# ------------------------------------------------------
# Plot RSME versus time
# ------------------------------------------------------

Temp_c5=np.zeros(len(Depth_matrix))
for i in range(0,len(Depth_matrix)):
    index_d=np.where(Depth_matrix[i]==5)
    if len(index_d[0])>0:
        Temp_c5[i]=Temp_matrix_c[i][index_d][0]
    if len(index_d[0])==0:
        Temp_c5[i]='nan'
        
        
Temp_c2=np.zeros(len(Depth_matrix))
for i in range(0,len(Depth_matrix)):
    index_d=np.where(Depth_matrix[i]==2)
    if len(index_d[0])>0:
        Temp_c2[i]=Temp_matrix_c[i][index_d][0]
    if len(index_d[0])==0:
        Temp_c2[i]='nan'
        
Temp_c0=np.zeros(len(Depth_matrix))
Depth_c0=np.zeros(len(Depth_matrix))
for i in range(0,len(Depth_matrix)):
    index_d=[[0]]
    if len(index_d[0])>0:
        Temp_c0[i]=Temp_matrix_c[i][index_d][0]
        Depth_c0[i]=Depth_matrix[i][index_d][0]
    if len(index_d[0])==0:
        Temp_c0[i]=Temp_matrix_c[i][index_d][0]
        Depth_c0[i]=Depth_matrix[i][index_d][0]
#%%
Time_vector=np.array(ctd_time)
Temp_vector=np.zeros(62)
Depth_vec=[]
cm = plt.cm.get_cmap('jet')

for i in range(0,len(Temp_matrix_s)):
    #RSME_vec.append(np.sqrt(np.mean((np.array(Temp_matrix_s[i])-np.array(Temp_matrix_c[i]))**2)))
    index=np.where(np.transpose(Depth_matrix[i])==5.)
    if len(index[0])>0:
        Temp_vector[i]=Temp_matrix_c[i][index[0]]
    if len(index[0])==0:
        Temp_vector[i]='nan'

Temp_vector2=[]
Time_vector2=[]
Lon2=[]
for i in range(0,len(Temp_vector)):
    if not isnan(Temp_vector[i]):
        Temp_vector2.append(Temp_vector[i])
        Time_vector2.append(Time_vector[i])
        Lon2.append(Lon_vec_c[i])

colors=Lon2
plt.figure(num=None, figsize=(8,4),dpi=1000, facecolor='w', edgecolor='k')
sc=plt.scatter(np.abs(Time_vector2),Temp_vector2, c=colors,alpha=0.75,s=150,cmap=cm,edgecolor='k',linewidth=1.5,vmin=-64.5,vmax=-62.5)
z=np.polyfit(np.abs(Time_vector2),Temp_vector2,1)
p=np.poly1d(z)
plt.plot(Time_vector2,p(Time_vector2),'k-',linewidth=3)
a=plt.colorbar(sc)
plt.ylabel(r'Temperature [$^0$C]',fontsize=15)
plt.xlabel('Time [h UTC]',fontsize=15)
plt.xlim([10,24.5])
plt.tick_params(axis='both', which='major', labelsize=15)
a.ax.tick_params(labelsize=15)
a.set_label(r'Longitude ($^0$W)',size=15)

savefig('CTD-UTC.pdf',bbox_inches='tight')

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
plt.plot(Temp_matrix_c[0],Depth_matrix[0],'k-',linewidth=2)
plt.plot(Temp_matrix_s[0],Depth_matrix[0], 'r-',linewidth=2)
plt.ylabel('Depth [m]',fontsize=15)
plt.xlabel('Temperature [K]',fontsize=15)
plt.tick_params(axis='both', which='major', labelsize=15)
#plt.ylim([max(list(depth_c)+list(depth_s)) + 5, min(list(depth_c)+list(depth_s)) - 0.5])
plt.ylim([np.max(Depth_matrix[0])+5,0])
plt.legend(['CTD','SCAMP','SCAMP, segmented'],loc='best')


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