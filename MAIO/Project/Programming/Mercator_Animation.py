# ------------------------------------------------------
# Preambule
# ------------------------------------------------------

from pylab import *
import numpy
import datetime
import time
import glob, os
import math
import netCDF4 as netcdf
from copy import copy
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap

# ------------------------------------------------------
# Read data
# ------------------------------------------------------
file='C:\Users\Mark\Documents\Studie\Data\MAIO_Project/Mercator_2h_august_18_september_7.nc'
DataSet = netcdf.Dataset(file, mode='r')

date	= DataSet.variables['time_counter'][:] 	#Hours passed since 1-1-1950, 00:00:00
lon		= DataSet.variables['longitude'][:] 	#Longitude (-80, -40)
lat 	= DataSet.variables['latitude'][:] 		#Latitude (0, 22)
u_vel	= DataSet.variables['u'][:] 			#Zonal velocity (m/s)
v_vel	= DataSet.variables['v'][:] 			#Meridional velocity (m/s)
#SSH	= DataSet.variables['ssh'][:] 			#SSH above Geoid (m)
temp	= DataSet.variables['temperature'][:] 	#Temperature (Kelvin)
DataSet.close()

# ------------------------------------------------------
# Focus on area of interest
# ------------------------------------------------------

lon2=lon[180:240+1]
lat2=lat[204:216+1]
temp2=[]
U2=[]
V2=[]
for i in range(0,len(temp)):
    dummy=[]
    dummyv=[]
    dummyu=[]
    for j in range(204,216+1):
        dummy.append(temp[i][j][180:240+1])
        dummyv.append(v_vel[i][j][180:240+1])
        dummyu.append(u_vel[i][j][180:240+1])
    temp2.append(dummy)
    U2.append(dummyu)
    V2.append(dummyv)
    
# ------------------------------------------------------
# Remove bad data (on the islands)
# ------------------------------------------------------
U3=np.array(U2)**2
V3=np.array(V2)**2
maxu=np.where(U3[0]==np.max(U3))
maxv=np.where(V3[0]==np.max(V3))
for i in range(0,len(U3)):
    U3[i][maxu]='nan'
    V3[i][maxv]='nan'

# ------------------------------------------------------
# Start Basemap
# ------------------------------------------------------

m = Basemap(
projection = 'merc',
llcrnrlat=17, urcrnrlat=18,
llcrnrlon=-65, urcrnrlon=-60,
resolution='i', area_thresh=0.01
) 
			
m.drawcoastlines(linewidth=0.2)
m.fillcontinents(color='#cc9966')

x,y=m(Lon_bath,Lat_bath)
c=plt.contour(x,y,-Depth,levels=[10,30,100,1000],cmap=plt.cm.Greys,norm=colors.LogNorm(vmin=3,vmax=10000))
par = m.drawparallels(np.arange(-80,81,0.5),labels=[1,0,0,0])
mer = m.drawmeridians(np.arange(-180,180,1),labels=[0,0,0,1])

# ------------------------------------------------------
# Start animation
# ------------------------------------------------------

from matplotlib import animation

x=0
t=2
U, V = U3[0], V3[0]

def init():
    b=temp2[0]
    imobj.set_data(b)
    time_text.set_text('time = 0:00')
    return imobj,time_text

def animate(self):
    global data
    global x
    global t
    global qk
    x += 1
    t += 2
    t = np.mod(t,24)
    a=temp2[x]
    imobj.set_data(a)
    au=U3[x]
    av=V3[x]
    
    time_text.set_text('time = %.0f:00' % t )
    
    Quivers.set_UVC(au,av)
    
    return imobj,time_text,Quivers
    
data=temp2[0]
my_cmap = copy(cm.get_cmap('jet'))
my_cmap.set_bad('white')
my_cmap.set_under('white')
imobj=m.imshow(data, cmap=my_cmap, animated=True, extent=[-65,-60,17,18],aspect=2,zorder=-1)

a=plt.colorbar(imobj,orientation='horizontal')
plt.clim(301.5,303.5)
time_text = plt.text(-64,17.5, '', zorder=10)

x2,y2=meshgrid(lon2,lat2)
xx,yy=m(x2,y2)

Quivers=m.quiver(xx,yy,U,V,units='inches',scale=0.6,pivot='tip',width=0.015,zorder=15)
qk = plt.quiverkey(Quivers, 0.5, 1.03, 0.5, r'$0.5 \frac{m}{s}$', labelpos='W',
                   fontproperties={'weight': 'bold'})
                   

anim = animation.FuncAnimation(plt.gcf(), animate, init_func=init,
                               frames=range(len(temp2)), interval=500)

plt.show()
