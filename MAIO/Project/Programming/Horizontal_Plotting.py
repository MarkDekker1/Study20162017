# ------------------------------------------------------
# Getting amount of CTD and 
# ------------------------------------------------------

which_depth=35 #meters
directory_CTD = 'C:\Users\Mark\Documents\Studie\MAIO_zip\MAIO/CTD_1m/'
CTD_files = glob.glob(directory_CTD+'*')
which_CTD_vec=np.arange(0,63,1)
which_SCAMP_vec=np.arange(0,36,1)
Depth_matrix=[]
Temp_matrix_s=[]
Lat_vec_s=[]
Lon_vec_s=[]
Temp_matrix_c=[]
Lat_vec_c=[]
Lon_vec_c=[]

# ------------------------------------------------------
# Start iteration
# ------------------------------------------------------
for number in range(0,len(which_CTD_vec)):
    if number<63:
        which_CTD=which_CTD_vec[number]
        which_SCAMP=1
    else:
        which_SCAMP=which_SCAMP_vec[number-63]
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

    if number<63:
        data=ReadData(Parameter_initial,comparison=To_compare,initialvalue=0)
        data.GetCTDData()
    else:
        data_c=ReadData(Parameter_initial,comparison=To_compare,initialvalue=0)
        data_c.GetCTDData()
        data_s=ReadData(Parameter_initial,comparison=To_compare,initialvalue=0)
        data_s.GetScampData()
        data_comp=ReadData(Parameter_initial,comparison=To_compare,initialvalue=0)
        data_comp.SegmentDataAtDepth(data_s.temp_acc,data_c.temp,data_s.depth,data_c.depth,which_depth)
    
# ------------------------------------------------------
# Save relevant data at every iteration
# ------------------------------------------------------
    
    if number<63:
        for j in range(0,len(data.depth)):
            if data.depth[j]==which_depth:
                Temp_matrix_c.append(data.temp[j])
                Lon_vec_c.append(data.lon)
                Lat_vec_c.append(data.lat)
                print(number)
    else:
        for j in range(0,len(data_comp.depth)):
            if data_comp.depth[j]==which_depth:
                if isnan(data_comp.temp_s[j])==False:
                    Temp_matrix_s.append(data_comp.temp_s[j])
                    Lon_vec_s.append(data_s.lon)
                    Lat_vec_s.append(data_s.lat)
                    print(number)

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
Temp1=Temp_matrix_c
Lon1=Lon_vec_c
Lat1=Lat_vec_c
#%%
Temp2=Temp_matrix_c
Lon2=Lon_vec_c
Lat2=Lat_vec_c
#%%
Temp3=Temp_matrix_c
Lon3=Lon_vec_c
Lat3=Lat_vec_c
#%%
Tempd=Temp_matrix_c
Lond=Lon_vec_c
Latd=Lat_vec_c

vmina=27.5
vmaxa=29.8

xi = np.linspace(np.min(Lond),np.max(Lond), 30)
yi = np.linspace(np.min(Latd),np.max(Latd),30)
zi = griddata(Lond,Latd, Tempd, xi, yi, interp='linear')

Matrix=np.zeros(shape=(len(yi),len(yi)))
for i in range(0,len(yi)):
    for j in range(0,len(xi)):
        if np.isnan(zi[i][j])==True:
            Matrix[i][j]==0
        else:
            Matrix[i][j]=zi[i][j]
AKA=plt.contourf(xi,yi,Matrix,25,vmin=vmina,vmax=vmaxa)

#%%
# ------------------------------------------------------
# Plot temperatures of CTD horizontally
# ------------------------------------------------------

matplotlib.style.use('classic')
from scipy.interpolate import griddata
from mpl_toolkits.basemap import Basemap
from matplotlib.mlab import griddata
import matplotlib.colors as colors

fig, (ax1,ax2,ax3)= plt.subplots(3,1,sharex=True,figsize=(10,8),dpi=1000)
#m = Basemap(projection = 'merc',
#llcrnrlat=17.2, urcrnrlat=17.9,
#llcrnrlon=-64.5, urcrnrlon=-60.3,
#resolution='i', area_thresh=0.001)

#vmina=27.3
#vmaxa=29.7
colormapused=plt.cm.jet
latmax=17.9
latmin=17.2
lonmax=-60
lonmin=-64.5
amountcolors=25
scattersize=10
levels_bath=[50,1000,5000]
amountcontours=8
alpha1=1


# ------------------------------------------------------
# Subplot 1
# ------------------------------------------------------

xi = np.linspace(np.min(Lon1),np.max(Lon1), 30)
yi = np.linspace(np.min(Lat1),np.max(Lat1),30)
zi = griddata(Lon1,Lat1, Temp1, xi, yi, interp='linear')

Matrix=np.zeros(shape=(len(yi),len(yi)))
for i in range(0,len(yi)):
    for j in range(0,len(xi)):
        if np.isnan(zi[i][j])==True:
            Matrix[i][j]==0
        else:
            Matrix[i][j]=zi[i][j]
        
x,y=(xi,yi)
c=ax1.contourf(x,y,Matrix,amountcolors,vmin=vmina,vmax=vmaxa,cmap=colormapused)
e=ax1.contour(x,y,Matrix,amountcontours,colors='k')
x1,y1=(Lon_bath,Lat_bath)
b=ax1.contour(x1,y1,-Depth,levels=levels_bath,colors='gray',norm=colors.LogNorm(vmin=3,vmax=10000),linewidth=0.5,zorder=11)
x1,y1=(Lon_bath,Lat_bath)
d=ax1.contourf(x1,y1,-Depth,levels=[0,5],colors='white',zorder=10)
ax1.set_ylabel('Latitude',fontsize=15)
lon,lat=(Lon1,Lat1)
ax1.scatter(lon,lat,s=scattersize,alpha=alpha1,c='k',zorder=2)
ax1.set_xlim([lonmin,lonmax])
ax1.set_ylim([latmin,latmax])
ax1.tick_params(axis='both', which='major', labelsize=15)

# ------------------------------------------------------
# Subplot 2
# ------------------------------------------------------

xi = np.linspace(np.min(Lon2),np.max(Lon2), 30)
yi = np.linspace(np.min(Lat2),np.max(Lat2),30)
zi = griddata(Lon2,Lat2, Temp2, xi, yi, interp='linear')

Matrix=np.zeros(shape=(len(yi),len(yi)))
for i in range(0,len(yi)):
    for j in range(0,len(xi)):
        if np.isnan(zi[i][j])==True:
            Matrix[i][j]==0
        else:
            Matrix[i][j]=zi[i][j]
        
x,y=(xi,yi)
c5=ax2.contourf(x,y,Matrix,amountcolors,vmin=vmina,vmax=vmaxa,cmap=colormapused)
e=ax2.contour(x,y,Matrix,amountcontours,colors='k')
x1,y1=(Lon_bath,Lat_bath)
b=ax2.contour(x1,y1,-Depth,levels=levels_bath,colors='gray',norm=colors.LogNorm(vmin=3,vmax=10000),linewidth=0.5,zorder=11)
x1,y1=(Lon_bath,Lat_bath)
d=ax2.contourf(x1,y1,-Depth,levels=[0,15],colors='white',zorder=10)
ax2.set_ylabel('Latitude',fontsize=15)
lon,lat=(Lon2,Lat2)
ax2.scatter(lon,lat,s=scattersize,alpha=alpha1,c='k')
ax2.set_xlim([lonmin,lonmax])
ax2.set_ylim([latmin,latmax])
ax2.tick_params(axis='both', which='major', labelsize=15)

# ------------------------------------------------------
# Subplot 3
# ------------------------------------------------------

xi = np.linspace(np.min(Lon3),np.max(Lon3), 30)
yi = np.linspace(np.min(Lat3),np.max(Lat3),30)
zi = griddata(Lon3,Lat3, Temp3, xi, yi, interp='linear')

Matrix=np.zeros(shape=(len(yi),len(yi)))
for i in range(0,len(yi)):
    for j in range(0,len(xi)):
        if np.isnan(zi[i][j])==True:
            Matrix[i][j]==0
        else:
            Matrix[i][j]=zi[i][j]
        
x,y=(xi,yi)
c=ax3.contourf(x,y,Matrix,amountcolors,vmin=vmina,vmax=vmaxa,cmap=colormapused)
e=ax3.contour(x,y,Matrix,amountcontours,colors='k')
x1,y1=(Lon_bath,Lat_bath)
b=ax3.contour(x1,y1,-Depth,levels=levels_bath,colors='gray',norm=colors.LogNorm(vmin=3,vmax=10000),linewidth=0.5,zorder=11)
x1,y1=(Lon_bath,Lat_bath)
d=ax3.contourf(x1,y1,-Depth,levels=[0,75],colors='white',zorder=10)
ax3.set_ylabel('Latitude',fontsize=15)
lon,lat=(Lon3,Lat3)
ax3.scatter(lon,lat,s=scattersize,alpha=alpha1,c='k')
ax3.set_xlim([lonmin,lonmax])
ax3.set_ylim([latmin,latmax])
ax3.tick_params(axis='both', which='major', labelsize=15)
ax3.set_xlabel('Longitude',fontsize=15)
c.set_clim(vmin=vmina,vmax=vmaxa)

# ---rest---

fig.subplots_adjust(right=0.8)
cbar_ax = fig.add_axes([0.85, 0.15, 0.05, 0.7])
v=np.linspace(vmina,vmaxa,amountcolors, endpoint=True)
a=fig.colorbar(AKA,cax=cbar_ax,extend='both')#,ticks=[27,30])#,norm=plt.colors.Normalize(vmin=vmina, vmax=vmaxa))

a.ax.tick_params(labelsize=15)
a.set_label(r'Temperature ($^0$C)',size=15)
savefig('Horizontal_all.pdf',bbox_inches='tight')