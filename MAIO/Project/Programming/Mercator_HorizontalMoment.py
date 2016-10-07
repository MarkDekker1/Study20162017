# ------------------------------------------------------
# Load data from Mercator Comparison
# ------------------------------------------------------

from copy import copy
index=index_vec[0]

# ------------------------------------------------------
# Read data
# ------------------------------------------------------

file='C:\Users\Mark\Documents\Studie\Data\MAIO_Project/Mercator_2h_august_18_september_7.nc'
DataSet = netcdf.Dataset(file, mode='r')

date	= DataSet.variables['time_counter'][index] 	#Hours passed since 1-1-1950, 00:00:00
lon		= DataSet.variables['longitude'][:] 	#Longitude (-80, -40)
lat 	= DataSet.variables['latitude'][:] 		#Latitude (0, 22)
u_vel	= DataSet.variables['u'][index] 			#Zonal velocity (m/s)
v_vel	= DataSet.variables['v'][index] 			#Meridional velocity (m/s)
#SSH	= DataSet.variables['ssh'][:] 			#SSH above Geoid (m)
temp	= DataSet.variables['temperature'][index] 	#Temperature (Kelvin)
DataSet.close()

# ------------------------------------------------------
# Focus on area of interest
# ------------------------------------------------------

lon2=lon[180:240+1]
lat2=lat[204:216+1]
temp2=[]
U2=[]
V2=[]
for j in range(204,216+1):
    temp2.append(temp[j][180:240+1])
    U2.append(v_vel[j][180:240+1])
    V2.append(u_vel[j][180:240+1])

    
# ------------------------------------------------------
# Remove bad data (on the islands)
# ------------------------------------------------------
U3=np.array(U2)**2
V3=np.array(V2)**2
maxu=np.where(U3==np.max(U3))
maxv=np.where(V3==np.max(V3))
for i in range(0,len(U3)):
    U3[maxu]='nan'
    V3[maxv]='nan'

# ------------------------------------------------------
# Start Basemap
# ------------------------------------------------------

plt.figure(figsize=(20,15))
m = Basemap(
projection = 'merc',
llcrnrlat=17, urcrnrlat=18,
llcrnrlon=-65, urcrnrlon=-60,
resolution='i', area_thresh=0.01
) 
			
m.drawcoastlines(linewidth=0.2)
m.fillcontinents(color='#cc9966')

x,y=m(Lon_bath,Lat_bath)
c=plt.contour(x,y,-Depth,levels=[10,30,100,1000],cmap=plt.cm.Greys,norm=colors.LogNorm(vmin=3,vmax=10000),linewidths=2)
par = m.drawparallels(np.arange(-80,81,0.5),labels=[1,0,0,0])
mer = m.drawmeridians(np.arange(-180,180,1),labels=[0,0,0,1])

x=0
t=2
U, V = U3, V3
    
my_cmap = copy(cm.get_cmap('jet'))
my_cmap.set_bad('white')
my_cmap.set_under('white')

x2,y2=meshgrid(lon2,lat2)
xx,yy=m(x2,y2)

cs=m.contourf(xx,yy,temp2,25)
c2=m.contour(xx,yy,temp2,25,colors='k',linewidths=0.5)
cbar = m.colorbar(cs, extend='both', location='bottom',pad="10%")#spacing='uniform'

plt.clim(301.5,303.5)
time_text = plt.text(-64,17.5, '', zorder=10)


Quivers=m.quiver(xx,yy,U,V,units='inches',scale=0.6,pivot='tip',width=0.015,zorder=15)
qk = plt.quiverkey(Quivers, 0.5, 1.03, 0.5, r'$0.5 \frac{m}{s}$', labelpos='W',
                   fontproperties={'weight': 'bold'})
x2,y2=m(data.lon,data.lat)
plt.scatter(x2,y2,s=100,c='m',zorder=15)

plt.show()
