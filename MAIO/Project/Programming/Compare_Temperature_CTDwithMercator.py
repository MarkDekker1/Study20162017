# ------------------------------------------------------
# Defining station-couples
# ------------------------------------------------------

which_CTD_vec=np.arange(0,63,1)#[15]
Temp_matrix_c=[]
Temp_matrix_m=[]
Temp_matrix_t=[]
Temp_vec_m0=[]
Time_matrix=[]
Depth_matrix_c=[]
SSH_matrix=[]
v_matrix=[]
u_matrix=[]
index_vec=[]

# ------------------------------------------------------
# Start iteration
# ------------------------------------------------------
for couple in range(0,len(which_CTD_vec)):
    which_CTD=which_CTD_vec[couple]

# ------------------------------------------------------
# Defining parameters
# ------------------------------------------------------
    
    Parameter_initial={
        'which_CTD':which_CTD
        }

# ------------------------------------------------------
# Get data
# ------------------------------------------------------

    data=Mercator(Parameter_initial,initialvalue=0)
    data.DataStation()

# ------------------------------------------------------
# Save data at every iteration
# ------------------------------------------------------
    
    Temp_matrix_c.append(data.temp_c)
    Depth_matrix_c.append(data.depth_c)
    Temp_vec_m0.append(data.temp_m0)
    Temp_matrix_m.append(data.temp_m)
    Time_matrix.append(data.hour)
    u_matrix.append(data.u_m)
    v_matrix.append(data.v_m)
    SSH_matrix.append(data.SSH)
    index_vec.append(data.index)
    print(couple)
    
# ------------------------------------------------------
# Take value of x m
# ------------------------------------------------------

Temp_c5=np.zeros(len(Depth_matrix_c))
for i in range(0,len(Depth_matrix_c)):
    index_d=np.where(Depth_matrix_c[i]==5)
    if len(index_d[0])>0:
        Temp_c5[i]=Temp_matrix_c[i][index_d][0]
    if len(index_d[0])==0:
        Temp_c5[i]='nan'
        
        
Temp_c2=np.zeros(len(Depth_matrix_c))
for i in range(0,len(Depth_matrix_c)):
    index_d=np.where(Depth_matrix_c[i]==2)
    if len(index_d[0])>0:
        Temp_c2[i]=Temp_matrix_c[i][index_d][0]
    if len(index_d[0])==0:
        Temp_c2[i]='nan'
        
Temp_c0=np.zeros(len(Depth_matrix_c))
Depth_c0=np.zeros(len(Depth_matrix_c))
for i in range(0,len(Depth_matrix_c)):
    index_d=[[0]]
    if len(index_d[0])>0:
        Temp_c0[i]=Temp_matrix_c[i][index_d][0]
        Depth_c0[i]=Depth_matrix_c[i][index_d][0]
    if len(index_d[0])==0:
        Temp_c0[i]=Temp_matrix_c[i][index_d][0]
        Depth_c0[i]=Depth_matrix_c[i][index_d][0]

#%%
# ------------------------------------------------------
# Plot scatter
# ------------------------------------------------------
plt.figure(num=None, figsize=(8,4),dpi=1000, facecolor='w', edgecolor='k')

cm = plt.cm.get_cmap('jet')
colors=np.linspace(Depth_c0[0],Depth_c0[len(Depth_c0)-1],len(Depth_c0))
sc=plt.scatter(np.array(Temp_c0),np.array(Temp_vec_m0)-273.15,s=100,alpha=0.6,zorder=15,c=colors,vmin=2,vmax=5,cmap=cm,linewidth=1, edgecolor='k')
a=plt.colorbar(sc)

#plt.scatter(np.array(Temp_c0),np.array(Temp_vec_m0)-273.15,s=100,c='r',alpha=1,zorder=15)
#plt.scatter(np.array(Temp_c2),np.array(Temp_vec_m0)-273.15,s=100,c='b',alpha=1,zorder=15)
#plt.scatter(np.array(Temp_c5),np.array(Temp_vec_m0)-273.15,s=100,c='k',alpha=1,zorder=15)
plt.plot([27,30], [27,30],'k')
plt.ylabel(r'Temperature Mercator [$^0$C]',fontsize=15)
plt.xlabel(r'Temperature CTD [$^0$C]',fontsize=15)
plt.xlim([29,30])
plt.ylim([29,30])
plt.tick_params(axis='both', which='major', labelsize=15)
a.ax.tick_params(labelsize=15)
a.set_label(r'Depth (m)',size=15)
savefig('Scatter_Mercator.pdf',bbox_inches='tight')

#%%
from scipy.stats import norm
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt

Error_matrix2=[]
for i in range(0,len(Temp_matrix_c)):
    Error_matrix2.append(np.transpose(np.array(Temp_c0))-(np.array(Temp_vec_m0)-273.15))

CHOOSE=Error_matrix2

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
plt.text(-0.75,4,'Mean',fontsize=15)
plt.text(-0.75,3.5,'Variance',fontsize=15)
#plt.text(-0.44,8,'-',fontsize=20)
plt.text(-0.4,4,round(mu,3),fontsize=15)
plt.text(-0.4,3.5,round(sigma**2.,3),fontsize=15)

plt.xlabel(r'Temperature error [$^0$C]',fontsize=15)
plt.xlim([-1,1])
plt.ylim([0,5])
plt.ylabel('Frequency',fontsize=15)
plt.tick_params(axis='both', which='major', labelsize=15)

savefig('PDF_Mercatorhighest.pdf',bbox_inches='tight')



#%%
# ------------------------------------------------------
# Plot Temperature versus time
# ------------------------------------------------------
    
fig, ax1 = plt.subplots(figsize=(8,4), edgecolor='k', facecolor='w')
ax1.plot(Time_matrix[0],Temp_matrix_m[0],'b-',linewidth='2')
plt.scatter(Time_matrix[0][index_vec[0]],Temp_matrix_m[0][index_vec[0]],s=100,c='g',alpha=1,zorder=15)
plt.scatter(Time_matrix[0][index_vec[0]],Temp_c0[0]+273.15,s=100,c='m',alpha=1,zorder=15)
ax1.set_xlabel('Time (h)',fontsize=15)
ax1.set_ylabel('Temperature Mercator [K]',fontsize=15,color='b')
for tl in ax1.get_yticklabels():
    tl.set_color('b')
ax2=ax1.twinx()
ax2.plot(Time_matrix[0],SSH_matrix[0],'r-',linewidth='2')
ax2.set_ylabel('SSH Mercator [m]',fontsize=15,color='r')
for tl in ax2.get_yticklabels():
    tl.set_color('r')
ax1.tick_params(axis='both', which='major', labelsize=15)
ax2.tick_params(axis='both', which='major', labelsize=15)

# ------------------------------------------------------
# Plot average daily cycle
# ------------------------------------------------------

time=np.arange(0,24,2)
Tav=[]
Sav=[]
for i in range(0,12):
    Tav.append(np.mean(Temp_matrix_m[0][np.arange(i,241,12)]))
    Sav.append(np.mean(SSH_matrix[0][np.arange(i,241,12)]))
    
fig, ax1 = plt.subplots(figsize=(8,4), edgecolor='k', facecolor='w')
ax1.plot(time,Tav,'b-',linewidth='2')
plt.scatter(np.mod(Time_matrix[0][index_vec[0]],24),Temp_matrix_m[0][index_vec[0]],s=100,c='g',alpha=1,zorder=15)
plt.scatter(np.mod(Time_matrix[0][index_vec[0]],24),Temp_c0[0]+273.15,s=100,c='m',alpha=1,zorder=15)
ax1.set_xlabel('Time (h)',fontsize=15)
ax1.set_ylabel('Temperature Mercator [K]',fontsize=15,color='b')
for tl in ax1.get_yticklabels():
    tl.set_color('b')
ax2=ax1.twinx()
ax2.plot(time,Sav,'r-',linewidth='2')
ax2.set_ylabel('SSH Mercator [m]',fontsize=15,color='r')
for tl in ax2.get_yticklabels():
    tl.set_color('r')
ax1.tick_params(axis='both', which='major', labelsize=15)
ax2.tick_params(axis='both', which='major', labelsize=15)

#%%
# ------------------------------------------------------
# Map
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

plt.figure(figsize=(15,15))
m = Basemap(projection = 'merc',
llcrnrlat=17, urcrnrlat=18.1,
llcrnrlon=-64.5, urcrnrlon=-60.3,
resolution='i', area_thresh=0.001)

x,y=m(Lon_bath,Lat_bath)
c=plt.contourf(x,y,-Depth,cmap=plt.cm.BrBG,levels=[10,15,20,25,50,100,250,500,750,1000,2000,3000,4000,5000,6000,7000],norm=colors.LogNorm(vmin=10,vmax=5000))
x2,y2=m(data.lon,data.lat)
plt.scatter(x2,y2,s=100,c='m')

cbar = m.colorbar(c,ticks=[1e1,1e2,1e3,1e4], extend='both', location='bottom',pad="10%")#spacing='uniform'

m.drawcoastlines(linewidth=0.2)
m.drawcountries()
m.drawmapboundary()
m.fillcontinents(color='#cc9966')
par = m.drawparallels(np.arange(15,20,0.5),labels=[1,0,0,0])
mer = m.drawmeridians(np.arange(-65,-59,1),labels=[0,0,0,1])