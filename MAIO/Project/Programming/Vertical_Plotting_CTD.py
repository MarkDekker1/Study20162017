# ------------------------------------------------------
# Choosing section
# ------------------------------------------------------
from scipy import interpolate
from scipy.interpolate import griddata
from mpl_toolkits.basemap import Basemap
from matplotlib.mlab import griddata
import matplotlib.colors as colors

which_SCAMP_vec=np.arange(0,35,1)
which_CTD_vec=[52,53,54,55,56,57,57,57,58,58,59,61,61,0,2,2,3,5,6,7,7,8,9,10,11,12,13,14,15,18,18,20,21,22,22]
Start1=0
End1=11
Start2=13
End2=23
Start3=27
End3=33
which_CTD_vec=which_CTD_vec[Start1:End1]

which_depth=10
Depth_matrix=[]
Temp_matrix=[]
Lat_vec_c=[]
Lon_vec_c=[]
Depth_vec=np.arange(0,4000,1)

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
    
#    f = interpolate.interp1d(z,T)    
#    
#    zmin = np.int(np.min(z))
#    zmax = np.int(np.max(z))
#    
#    znew=np.zeros(len(Depth_vec))
#    for i in range(0,len(Depth_vec)):
#        if i<zmin:
#            znew[i]='nan'
#        if i>=zmin and i<zmax:
#            znew[i]=f(Depth_vec[zmin:zmax])[i-zmin]
#        if i>=zmax:
#            znew[i]='nan'
#    
#    Temp_matrix.append(znew)
#    Depth_matrix.append(Depth_vec[zmin:zmax])
    Temp_matrix.append(T)
    Depth_matrix.append(z)
    
    
    print(number)
#%%
Temp1=Temp_matrix
Depth1=Depth_matrix
Lon1=Lon_vec_c
Lat1=Lat_vec_c
Stations1=which_CTD_vec
Stations1_s=[1,2,3,4,5,6,7,8]
#%%
Temp2=Temp_matrix
Depth2=Depth_matrix
Lon2=Lon_vec_c
Lat2=Lat_vec_c
Stations2=which_CTD_vec
Stations2_s=[11,12,13,14,15,16,18,17]
#%%
Temp3=Temp_matrix
Depth3=Depth_matrix
Lon3=Lon_vec_c
Lat3=Lat_vec_c
Stations3=which_CTD_vec
Stations3_s=[21,22,23,24,25]

#%%
Temp1=Temp2
Depth1=Depth2
Lon1=Lon2
Lat1=Lat2
Stations1=Stations2
Stations1_s=Stations2_s
#%%
Temp1=Temp3
Depth1=Depth3
Lon1=Lon3
Lat1=Lat3
Stations1=Stations3
Stations1_s=Stations3_s
#%%
# ------------------------------------------------------
# Singleplot
# ------------------------------------------------------

def Distance(lat1,lat2,lon1,lon2):
    difvert=np.abs(lat2-lat1)/360.*2.*np.pi*6371.*1000.
    difhor=np.abs(lon2-lon1)/360.*2.*np.pi*6371.*1000.*cos(np.mean([lat2,lat1])/360.*2.*np.pi)
    return np.sqrt(difvert**2+difhor**2)/1000.

def MaximaMatrix(A):
    vec=[]
    for i in range(0,len(A)):
        vec.append(max(A[i]))
    return vec

#%%
# ------------------------------------------------------
# Get Bathymetry at locations
# ------------------------------------------------------

fig= plt.figure(figsize=(10,12))
deepest1=50#50#4000
deepest2=50#50#1000
deepest3=75#75#1000
colorbarused=plt.cm.rainbow#rainbow#coolwarm
colorstationlines='white'
colorbottom='k'
transparency=0.7#0.7#0.0
OrderContour=15
Amountcontours=15
vmina=27.5#27.5#4
vmaxa=30

# ------------------------------------------------------
# Transect 1
# ------------------------------------------------------

plt.subplot(311)
end=len(Lat1)-1
Horvec=np.linspace(0,Distance(Lat1[end],Lat1[0],Lon1[end],Lon1[0]),1000)

data=ReadData(Parameter_initial,comparison=To_compare,initialvalue=0)
data.GetStraightBathymetry(Lat1[end],Lat1[0],Lon1[end],Lon1[0],1000)
a=data.Depth_vector

Stations_dist=[]
for i in range(0,len(Stations1)):
    Stations_dist.append(Distance(Lat1[0],Lat1[i],Lon1[0],Lon1[i]))
xi = np.linspace(np.min(Stations_dist),np.max(Stations_dist), 1000)
yi = np.linspace(2,deepest1,1000)
points = np.transpose([np.array(Stations_dist),Depth_vec])

xvec=[]
yvec=[]
temp1_new=[]
for i in range(0,len(Stations_dist)):
    for j in range(0,len(Depth1[i])):
        xvec.append(Stations_dist[i])
        yvec.append(Depth1[i][j])
        temp1_new.append(Temp1[i][j])

zi = griddata(xvec,yvec, temp1_new, xi, yi, interp='linear')

cs=plt.contourf(xi,-yi,zi,100,cmap=colorbarused,zorder=5,vmin=vmina,vmax=vmaxa)
#cb=plt.colorbar(cs)
#plt.clim([13,30])
plt.contour(xi,-yi,zi,Amountcontours,zorder=OrderContour,colors='k')
plt.scatter(Stations_dist,-np.array(MaximaMatrix(Depth1)),s=75,c='orange',alpha=1,zorder=52,edgecolor='k',linewidth=2,label='Measuring Stations')
for i in range(0,len(Stations_dist)):
    ind=Stations_dist[i]
    plt.plot([ind,ind], [-deepest1,0],'--',color=colorstationlines,linewidth=2,zorder=51)

plt.fill_between(Horvec[::-1], -10000, a, facecolor=colorbottom,zorder=50)#saddlebrown
plt.plot(Horvec[::-1],a,'k',linewidth=3,zorder=51)

f=interpolate.interp1d(Stations_dist,MaximaMatrix(Depth1))
a=f(Horvec)
#plt.fill_between(Horvec, -10000, -a, facecolor='white',alpha=transparency,zorder=25)#saddlebrown


plt.ylim([-deepest1,-2])
plt.xlim([0,max(Horvec)])
#plt.xlabel('Horizontal distance (m)',fontsize=15)
plt.ylabel('Depth (m)',fontsize=15)
plt.tick_params(axis='both', which='major', labelsize=15)



# ------------------------------------------------------
# Transect 2
# ------------------------------------------------------

plt.subplot(312)
end=len(Lat2)-1
Horvec=np.linspace(0,Distance(Lat2[end],Lat2[0],Lon2[end],Lon2[0]),1000)

data=ReadData(Parameter_initial,comparison=To_compare,initialvalue=0)
data.GetStraightBathymetry(Lat2[end],Lat2[0],Lon2[end],Lon2[0],1000)
a=data.Depth_vector

Stations_dist=[]
for i in range(0,len(Stations2)):
    Stations_dist.append(Distance(Lat2[0],Lat2[i],Lon2[0],Lon2[i]))
xi = np.linspace(np.min(Stations_dist),np.max(Stations_dist), 1000)
yi = np.linspace(2,deepest2,1000)
points = np.transpose([np.array(Stations_dist),Depth_vec])

xvec=[]
yvec=[]
temp2_new=[]
for i in range(0,len(Stations_dist)):
    for j in range(0,len(Depth2[i])):
        xvec.append(Stations_dist[i])
        yvec.append(Depth2[i][j])
        temp2_new.append(Temp2[i][j])

zi = griddata(xvec,yvec, temp2_new, xi, yi, interp='linear')

cs2=plt.contourf(xi,-yi,zi,100,cmap=colorbarused,zorder=5,vmin=vmina,vmax=vmaxa)
#cb=plt.colorbar(cs)
#plt.clim([13,30])
plt.contour(xi,-yi,zi,Amountcontours,zorder=OrderContour,colors='k')
plt.scatter(Stations_dist,-np.array(MaximaMatrix(Depth2)),s=75,c='orange',alpha=1,zorder=52,edgecolor='k',linewidth=2,label='Measuring Stations')
for i in range(0,len(Stations_dist)):
    ind=Stations_dist[i]
    plt.plot([ind,ind], [-deepest2,0],'--',color=colorstationlines,linewidth=2,zorder=51)

plt.fill_between(Horvec[::-1], -10000, a, facecolor=colorbottom,zorder=50)#saddlebrown
plt.plot(Horvec[::-1],a,'k',linewidth=3,zorder=51)
f=interpolate.interp1d(Stations_dist,MaximaMatrix(Depth2))
a=f(Horvec)
#plt.fill_between(Horvec, -10000, -a, facecolor='white',alpha=transparency,zorder=25)#saddlebrown
plt.ylim([-deepest2,-2])
plt.xlim([0,max(Horvec)])
#plt.xlabel('Horizontal distance (m)',fontsize=15)
plt.ylabel('Depth (m)',fontsize=15)
plt.tick_params(axis='both', which='major', labelsize=15)



# ------------------------------------------------------
# Transect 3
# ------------------------------------------------------


plt.subplot(313)
end=len(Lat3)-1
Horvec=np.linspace(0,Distance(Lat3[end],Lat3[0],Lon3[end],Lon3[0]),1000)

data=ReadData(Parameter_initial,comparison=To_compare,initialvalue=0)
data.GetStraightBathymetry(Lat3[end],Lat3[0],Lon3[end],Lon3[0],1000)
a=data.Depth_vector

Stations_dist=[]
for i in range(0,len(Stations3)):
    Stations_dist.append(Distance(Lat3[0],Lat3[i],Lon3[0],Lon3[i]))
xi = np.linspace(np.min(Stations_dist),np.max(Stations_dist), 1000)
yi = np.linspace(2,deepest3,1000)
points = np.transpose([np.array(Stations_dist),Depth_vec])

xvec=[]
yvec=[]
temp3_new=[]
for i in range(0,len(Stations_dist)):
    for j in range(0,len(Depth3[i])):
        xvec.append(Stations_dist[i])
        yvec.append(Depth3[i][j])
        temp3_new.append(Temp3[i][j])

zi = griddata(xvec,yvec, temp3_new, xi, yi, interp='linear')

#cs=plt.contourf(Stations_dist,-Depth_vec[2:],np.transpose(Temp3)[2:],100)
cs3=plt.contourf(xi,-yi,zi,100,cmap=colorbarused,vmin=vmina,vmax=vmaxa,zorder=5)
#cb=plt.colorbar(cs)
plt.contour(xi,-yi,zi,Amountcontours,zorder=OrderContour,colors='k')
plt.scatter(Stations_dist,-np.array(MaximaMatrix(Depth3)),s=75,c='orange',alpha=1,zorder=52,edgecolor='k',linewidth=2,label='Measuring Stations')
for i in range(0,len(Stations_dist)):
    ind=Stations_dist[i]
    plt.plot([ind,ind], [-deepest3,0],'--',color=colorstationlines,linewidth=2,zorder=51)

plt.fill_between(Horvec[::-1], -10000, a, facecolor=colorbottom,zorder=50)#saddlebrown
plt.plot(Horvec[::-1],a,'k',linewidth=3,zorder=51)
f=interpolate.interp1d(Stations_dist,MaximaMatrix(Depth3))
a=f(Horvec)
#plt.fill_between(Horvec, -10000, -a, facecolor='white',alpha=transparency,zorder=25)#saddlebrown

plt.ylim([-deepest3,-2])
plt.xlim([0,max(Horvec)])
plt.xlabel('Horizontal distance (km)',fontsize=15)
plt.ylabel('Depth (m)',fontsize=15)
plt.tick_params(axis='both', which='major', labelsize=15)

fig.subplots_adjust(right=0.8)
cbar_ax = fig.add_axes([0.85, 0.15, 0.05, 0.7])
a=fig.colorbar(cs3, cax=cbar_ax)
a.ax.tick_params(labelsize=15)
a.set_label(r'Temperature ($^0$C)',size=15)

#%%
# ------------------------------------------------------
# Triplot
# ------------------------------------------------------
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
    
# ------------------------------------------------------
# Plot temperatures of CTD vertically
# ------------------------------------------------------
    
from scipy.interpolate import griddata
from mpl_toolkits.basemap import Basemap
from matplotlib.mlab import griddata
import matplotlib.colors as colors

plt.figure(figsize=(10,5))

plt.subplot(131)
for i in range(0,len(Lon1)):
    more=where(Lon_bath>=Lon1[i]-Distance)
    less=where(Lon_bath<=Lon1[i]+Distance)
    commons_lon.append(np.intersect1d(more,less)[0])
    
commons_lat=[]
for j in range(0,len(Lat1)):
    more=where(Lat_bath>=Lat1[j]-Distance)
    less=where(Lat_bath<=Lat1[j]+Distance)
    commons_lat.append(np.intersect1d(more,less)[0])

stations_depth=[]
for i in range(0,len(Lat1)):
    stations_depth.append(Depth[commons_lat[i],commons_lon[i]])
    
c=plt.contourf(Station_vec,-Depth_vec[2:],np.transpose(Temp1)[2:],100)
c2=plt.contour(Station_vec,-Depth_vec[2:],np.transpose(Temp1)[2:],25,zorder=15,colors='k')
plt.plot(Station_vec,stations_depth,'k',linewidth=2,zorder=50)
plt.fill_between(Station_vec, -10000, stations_depth, facecolor='saddlebrown',zorder=50)
plt.ylim([-np.max(Depth_vec),-2])
plt.colorbar(c)
plt.clim([27,30])
plt.ylabel('Depth [m]',fontsize=15)
plt.xlabel('Station Number',fontsize=15)
plt.tick_params(axis='both', which='major', labelsize=15)

plt.subplot(231)

for i in range(0,len(Lon2)):
    more=where(Lon_bath>=Lon2[i]-Distance)
    less=where(Lon_bath<=Lon2[i]+Distance)
    commons_lon.append(np.intersect1d(more,less)[0])
    
commons_lat=[]
for j in range(0,len(Lat2)):
    more=where(Lat_bath>=Lat2[j]-Distance)
    less=where(Lat_bath<=Lat2[j]+Distance)
    commons_lat.append(np.intersect1d(more,less)[0])

stations_depth=[]
for i in range(0,len(Lat2)):
    stations_depth.append(Depth[commons_lat[i],commons_lon[i]])
    
c=plt.contourf(Station_vec,-Depth_vec[2:],np.transpose(Temp2)[2:],100)
c2=plt.contour(Station_vec,-Depth_vec[2:],np.transpose(Temp2)[2:],25,zorder=15,colors='k')
plt.plot(Station_vec,stations_depth,'k',linewidth=2,zorder=50)
plt.fill_between(Station_vec, -10000, stations_depth, facecolor='saddlebrown',zorder=50)
plt.ylim([-np.max(Depth_vec),-2])
plt.colorbar(c)
plt.clim([27,30])
plt.ylabel('Depth [m]',fontsize=15)
plt.xlabel('Station Number',fontsize=15)
plt.tick_params(axis='both', which='major', labelsize=15)

plt.subplot(331)

for i in range(0,len(Lon3)):
    more=where(Lon_bath>=Lon3[i]-Distance)
    less=where(Lon_bath<=Lon3[i]+Distance)
    commons_lon.append(np.intersect1d(more,less)[0])
    
commons_lat=[]
for j in range(0,len(Lat3)):
    more=where(Lat_bath>=Lat3[j]-Distance)
    less=where(Lat_bath<=Lat3[j]+Distance)
    commons_lat.append(np.intersect1d(more,less)[0])

stations_depth=[]
for i in range(0,len(Lat3)):
    stations_depth.append(Depth[commons_lat[i],commons_lon[i]])
    
c=plt.contourf(Station_vec,-Depth_vec[2:],np.transpose(Temp3)[2:],100)
c2=plt.contour(Station_vec,-Depth_vec[2:],np.transpose(Temp3)[2:],25,zorder=15,colors='k')
plt.plot(Station_vec,stations_depth,'k',linewidth=2,zorder=50)
plt.fill_between(Station_vec, -10000, stations_depth, facecolor='saddlebrown',zorder=50)
plt.ylim([-np.max(Depth_vec),-2])
plt.colorbar(c)
plt.clim([27,30])
plt.ylabel('Depth [m]',fontsize=15)
plt.xlabel('Station Number',fontsize=15)
plt.tick_params(axis='both', which='major', labelsize=15)