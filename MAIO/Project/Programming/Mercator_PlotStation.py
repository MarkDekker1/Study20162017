from pylab import *
import numpy
import datetime
import time
import glob, os
import math
import netCDF4 as netcdf
import matplotlib.pyplot as plt
#from mpl_toolkits.basemap import Basemap


DataSet = netcdf.Dataset('Mercator_2h_august_18_september_7.nc', mode='r')

date	= DataSet.variables['time_counter'][:] 	#Hours passed since 1-1-1950, 00:00:00
lon		= DataSet.variables['longitude'][:] 	#Longitude (-80, -40)
lat 	= DataSet.variables['latitude'][:] 		#Latitude (0, 22)
u_vel	= DataSet.variables['u'][:] 			#Zonal velocity (m/s)
v_vel	= DataSet.variables['v'][:] 			#Meridional velocity (m/s)
#SSH	= DataSet.variables['ssh'][:] 			#SSH above Geoid (m)
temp	= DataSet.variables['temperature'][:] 	#Temperature (Kelvin)

DataSet.close()
#%%
for i in range(0,5):
    for j in range(0,len(temp[0])):
        for k in range(0,len(temp[0][0])):
            if temp[i][j][k]<0:
                temp[i][j][k]='nan'
    print(i)
#%% Cut out data
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

    
#%% Animation
from matplotlib import animation

# First set up the figure, the axis, and the plot element we want to animate
fig = plt.figure()
#ax = plt.axes(xlim=(0, L), ylim=(-0.5,2))
#line, = ax.plot([], [], lw=2)
x=0
t=2

U, V = U2[0], V2[0]

# initialization function: plot the background of each frame
def init():
    b=temp2[0]
    imobj.set_data(b[::-1])
    time_text.set_text('time = 0:00')
    return imobj,time_text

# animation function.  This is called sequentially
def animate(self):
    global data
    global x
    global t
    global qk
    x += 1
    t += 2
    t = np.mod(t,24)
    a=temp2[x]
    imobj.set_data(a[::-1])
    au=U2[x]
    av=V2[x]
    #imobj.set_data(au[::-1])
    
    time_text.set_text('time = %.0f:00' % t )
    #imobj.set_zorder(0)
    
    Quivers.set_UVC(au,av)
    qk = plt.quiverkey(Quivers, 0.5, 1.03, 0.5, r'$0.5 \frac{m}{s}$', labelpos='W',
                       fontproperties={'weight': 'bold'})
    
    return imobj,time_text,Quivers,qk
    
c=temp2[0]
data=c[::-1]
imobj=plt.imshow(data, cmap='jet', animated=True, extent=[-65,-60,17,18],aspect=2)
#ax.set_aspect(2)#,aspect=0.5,extent=[0, 2.0, 0.0, 2.0], alpha=1.0, zorder=1)

plt.colorbar(orientation='horizontal')
plt.clim(301.5,303.5)

time_text = plt.text(-65,18, '', zorder=10)

Quivers=plt.quiver(lon2,lat2,U,V,units='x',
               pivot='tip',
               width=0.012,
               scale=1 / 0.5)
qk = plt.quiverkey(Quivers, 0.5, 1.03, 0.5, r'$0.5 \frac{m}{s}$', labelpos='W',
                   fontproperties={'weight': 'bold'})

# call the animator.  blit=True means only re-draw the parts that have changed.
anim = animation.FuncAnimation(fig, animate, init_func=init,
                               frames=range(len(temp2)), interval=500)

plt.show()
#%%
Hours=np.mod(date-date[0],24)



#%%
#Time begin = 18/08/2016 01:00:00, Time stop = 7/09/2016 01:00:00
my_datetime = datetime.datetime(year=2016, month=8, day=18).toordinal() + 1.0/24.0
date 		= my_datetime + (date - date[0]) / 24.0 #Date array is now in toordinal form with the correct time


m = Basemap(
projection = 'merc',
llcrnrlat=17, urcrnrlat=18.1,
llcrnrlon=-64, urcrnrlon=-62,
resolution='i', area_thresh=0.01
) 
			
m.fillcontinents()
m.drawcoastlines(linewidth=0.2)
par = m.drawparallels(np.arange(-80,81,1),labels=[1,0,0,0])
mer = m.drawmeridians(np.arange(-180,180,1),labels=[0,0,0,1])

x,y = meshgrid(lon,lat)
x,y = m(x,y)

u_vel_example, v_vel_example = u_vel[0], v_vel[0]
Q = m.quiver(x,y,u_vel_example, v_vel_example,scale=7)
show()