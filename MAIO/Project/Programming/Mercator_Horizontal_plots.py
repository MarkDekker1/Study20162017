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
import matplotlib.colors as colors

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
U2=np.array(U2)
V2=np.array(V2)
temp2=np.array(temp2)

# ------------------------------------------------------
# Remove bad data (on the islands)
# ------------------------------------------------------
U2=np.array(U2)**2
V2=np.array(V2)**2

for i in range(0,len(U2)):
    maxu=np.where(U2[i]>30)
    maxv=np.where(V2[i]>30)
    weirdT=np.where(temp2[i]==-32767.0)
    
    for j in range(0,len(maxu[0])):
        U2[i,maxu[0][j],maxu[1][j]]='nan'
    for j in range(0,len(maxv[0])):
        V2[i,maxv[0][j],maxv[1][j]]='nan'
    for j in range(0,len(weirdT[0])):
        temp2[i,weirdT[0][j],weirdT[1][j]]='nan'

# ------------------------------------------------------
# Take averages and variances
# ------------------------------------------------------
#%%
temp2_var=zeros(shape=(13,61))
temp2_mean=zeros(shape=(13,61))
U2_var=zeros(shape=(13,61))
U2_mean=zeros(shape=(13,61))
V2_var=zeros(shape=(13,61))
V2_mean=zeros(shape=(13,61))
Velo_var=zeros(shape=(13,61))
Fourier_matrix=[]
Freq_vec = np.fft.fftfreq(len(temp2),d=2)
Time_vec = []
Fourier_24=zeros(shape=(13,61))
Fourier_12=zeros(shape=(13,61))
Fourier_higher=zeros(shape=(13,61))
Fourier_24V=zeros(shape=(13,61))
Fourier_12V=zeros(shape=(13,61))
Fourier_higherV=zeros(shape=(13,61))
for i in range(0,len(Freq_vec)):
    Time_vec.append(1./Freq_vec[i])

for j in range(0,len(temp2[0])):
    for k in range(0,len(temp2[0,0])):
        temp2_mean[j,k]=np.mean(temp2[:,j,k])
        temp2_var[j,k]=np.var(temp2[:,j,k])
        U2_mean[j,k]=np.mean(U2[:,j,k])
        U2_var[j,k]=np.var(U2[:,j,k])
        V2_mean[j,k]=np.mean(V2[:,j,k])
        V2_var[j,k]=np.var(V2[:,j,k])
        Velo_var[j,k]=np.var(np.sqrt(U2[:,j,k]**2.+V2[:,j,k]**2.))
        a=np.abs(np.fft.fft(temp2[:,j,k]))**2.
        b=np.abs(np.fft.fft(np.sqrt(U2[:,j,k]**2.+V2[:,j,k]**2.)))**2.
        Fourier_matrix.append(sum(a))
        Fourier_24[j,k]=np.sum(a[18:23]/sum(a))
        Fourier_12[j,k]=np.sum(a[38:43]/sum(a))
        Fourier_higher[j,k]=np.sum(a[1:15]/sum(a))
        Fourier_24V[j,k]=np.sum(b[18:23]/sum(b))
        Fourier_12V[j,k]=np.sum(b[38:43]/sum(b))
        Fourier_higherV[j,k]=np.sum(b[1:15]/sum(b))
        

#%%
# ------------------------------------------------------
# Plot
# ------------------------------------------------------

Tempplot=temp2_mean
Uplot=U2_mean
Vplot=V2_mean

Tempvarplot=temp2_var
Uvarplot=U2_var
Vvarplot=V2_var
Velovarplot=Velo_var

fig, (ax1,ax2)= plt.subplots(2,1,sharex=True,figsize=(10,8))

vmina=29
vmaxa=29.6
vminb=0.034
vmaxb=0.096
vminc=9.7e-05
vmaxc=0.001
colormapused='rainbow'
latmax=17.9
latmin=17.2
lonmax=-60
lonmin=-64.5
amountcolors=25
Quiversize=0.5
Quivertitle=r'$0.5 m/s$'
contours=[2e-4,3e-4,4e-4,8e-4,12e-4,50e-4,1e-2,5e-2]
alphacont=0.3

my_cmap = copy(cm.get_cmap(colormapused))
my_cmap.set_bad('white')
my_cmap.set_under('white')

#Plot 1

c=ax1.contourf(lon2,lat2,Tempplot-273.15,amountcolors,vmin=vmina,vmax=vmaxa,cmap=colormapused)
x1,y1=(Lon_bath,Lat_bath)
b=ax1.contour(x1,y1,-Depth,levels=[10,30,100,1000],cmap=plt.cm.Greys,norm=colors.LogNorm(vmin=3,vmax=10000))
x1,y1=(Lon_bath,Lat_bath)
d=ax1.contourf(x1,y1,-Depth,levels=[0,5],colors='white')
ax1.set_ylabel('Latitude',fontsize=15)
ax1.set_xlim([lonmin,lonmax])
ax1.set_ylim([latmin,latmax])
ax1.tick_params(axis='both', which='major', labelsize=15)
Quivers=ax1.quiver(lon2,lat2,Uplot,Vplot,units='inches',scale=Quiversize,pivot='tip',width=0.015,zorder=15)
qk = ax1.quiverkey(Quivers, 0.5, 1.03, Quiversize, Quivertitle, labelpos='W',fontproperties={'weight': 'bold'})
fig.subplots_adjust(right=0.8)
cbar_ax = fig.add_axes([0.85, 0.55, 0.05, 0.3])
a=fig.colorbar(c,cax=cbar_ax)
a.ax.tick_params(labelsize=15)
a.set_label(r'Mean Temperature ($^0$C)',size=15)

#Plot 2
large=np.where(Velovarplot>1e2)
small=np.where(Velovarplot<1e-5)

c=ax2.contourf(lon2,lat2,Tempvarplot,amountcolors,vmin=vminb,vmax=vmaxb,cmap=colormapused)
k=ax2.contour(lon2,lat2,Velovarplot,levels=contours,vmin=vminc,vmax=vmaxc,colors='k',zorder=25)
x1,y1=(Lon_bath,Lat_bath)
b=ax2.contour(x1,y1,-Depth,levels=[10,30,100,1000],cmap=plt.cm.Greys,norm=colors.LogNorm(vmin=3,vmax=10000))
x1,y1=(Lon_bath,Lat_bath)
d=ax2.contourf(x1,y1,-Depth,levels=[0,5],colors='white')
ax2.set_ylabel('Latitude',fontsize=15)
ax2.set_xlim([lonmin,lonmax])
ax2.set_ylim([latmin,latmax])
ax2.tick_params(axis='both', which='major', labelsize=15)
ax2.set_xlabel('Longitude',fontsize=15)
fig.subplots_adjust(right=0.8)
cbar_ax = fig.add_axes([0.85, 0.15, 0.05, 0.3])
a=fig.colorbar(c,cax=cbar_ax)
a.ax.tick_params(labelsize=15)
a.set_label(r'Variance Temperature ($^0$C$^2$)',size=15)
ax2.contourf(lon2,lat2,Velovarplot,levels=[8e-4,100000],colors=['black','white'],alpha=alphacont,zorder=35)


#%%
fig, (ax1,ax2,ax3)= plt.subplots(3,1,sharex=True,figsize=(10,8))

factor1=-8.1
factor2=-6.5
amountcolors=100
colormapused=plt.cm.rainbow

#vmina=1*10**factor1
#vmaxa=1*10**factor2
#leveling=[1e-9,5e-9,1e-8,5e-8,1e-7,5e-7,1e-6]
#leveling=np.logspace(factor1,factor2,amountcolors)
#
#vmina=10**-8.1
#vmaxa=10**-7.6
#
#vminb=10**-7.5
#vmaxb=10**-6.9
#
#vminc=10**-7.5
#vmaxb=10**-6.5

lowa=10**-3.1
lowb=10**-1.9
lowc=10**-0.7
alphacont=0.3
amountcontours=5
contoursa=np.logspace(-4,-2,amountcontours)
contoursb=np.logspace(-3,-1,amountcontours)
contoursc=np.logspace(-2,0,amountcontours)
contoursa=[lowa,10000]
contoursb=[lowb,10000]
contoursc=[lowc,10000]

#Plot 1
c=ax1.contourf(lon2,lat2,Fourier_12,amountcolors,cmap=colormapused)#,vmin=vmina,vmax=vmaxa)#,norm=colors.LogNorm(vmin=vmina,vmax=vmaxa))
k=ax1.contour(lon2,lat2,Fourier_12V,levels=contoursa,colors='k',zorder=25)
ax1.contourf(lon2,lat2,Fourier_12V,levels=[lowa,100000],colors=['black','white'],alpha=alphacont,zorder=35)

x1,y1=(Lon_bath,Lat_bath)
b=ax1.contour(x1,y1,-Depth,levels=[10,30,100,1000],cmap=plt.cm.Greys,norm=colors.LogNorm(vmin=3,vmax=10000))
x1,y1=(Lon_bath,Lat_bath)
d=ax1.contourf(x1,y1,-Depth,levels=[0,5],colors='white')
ax1.set_ylabel('Latitude',fontsize=15)
ax1.set_xlim([lonmin,lonmax])
ax1.set_ylim([latmin,latmax])
ax1.tick_params(axis='both', which='major', labelsize=15)

fig.subplots_adjust(right=0.8)
cbar_ax = fig.add_axes([0.85, 0.66, 0.05, 0.25])
a=fig.colorbar(c,cax=cbar_ax)
a.ax.tick_params(labelsize=15)
a.set_label(r'12 h cycle',size=15)

#Plot 2
c=ax2.contourf(lon2,lat2,Fourier_24,amountcolors,cmap=colormapused)#,vmin=vminb,vmax=vmaxb)#,levels=leveling,norm=colors.LogNorm(vmin=vmina,vmax=vmaxa),cmap=colormapused)
x1,y1=(Lon_bath,Lat_bath)
k=ax2.contour(lon2,lat2,Fourier_24V,levels=contoursb,colors='k',zorder=25)
ax2.contourf(lon2,lat2,Fourier_24V,levels=[lowb,100000],colors=['black','white'],alpha=alphacont,zorder=35)

b=ax2.contour(x1,y1,-Depth,levels=[10,30,100,1000],cmap=plt.cm.Greys,norm=colors.LogNorm(vmin=3,vmax=10000))
x1,y1=(Lon_bath,Lat_bath)
d=ax2.contourf(x1,y1,-Depth,levels=[0,5],colors='white')
ax2.set_ylabel('Latitude',fontsize=15)
ax2.set_xlim([lonmin,lonmax])
ax2.set_ylim([latmin,latmax])
ax2.tick_params(axis='both', which='major', labelsize=15)

fig.subplots_adjust(right=0.8)
cbar_ax = fig.add_axes([0.85, 0.38, 0.05, 0.25])
a=fig.colorbar(c,cax=cbar_ax)
a.ax.tick_params(labelsize=15)
a.set_label(r'24 h cycle',size=15)

#Plot 3
c=ax3.contourf(lon2,lat2,Fourier_higher,amountcolors,cmap=colormapused)#,vmin=vminc,vmax=vmaxc)#levels=leveling,norm=colors.LogNorm(vmin=vmina,vmax=vmaxa),cmap=colormapused)
x1,y1=(Lon_bath,Lat_bath)
k=ax3.contour(lon2,lat2,Fourier_higherV,levels=contoursc,colors='k',zorder=25)
ax3.contourf(lon2,lat2,Fourier_higherV,levels=[lowc,100000],colors=['black','white'],alpha=alphacont,zorder=35)

b=ax3.contour(x1,y1,-Depth,levels=[10,30,100,1000],cmap=plt.cm.Greys,norm=colors.LogNorm(vmin=3,vmax=10000))
x1,y1=(Lon_bath,Lat_bath)
d=ax3.contourf(x1,y1,-Depth,levels=[0,5],colors='white')
ax3.set_ylabel('Latitude',fontsize=15)
ax3.set_xlim([lonmin,lonmax])
ax3.set_ylim([latmin,latmax])
ax3.tick_params(axis='both', which='major', labelsize=15)
ax3.set_xlabel('Longitude',fontsize=15)

fig.subplots_adjust(right=0.8)
cbar_ax = fig.add_axes([0.85, 0.1, 0.05, 0.25])
a=fig.colorbar(c,cax=cbar_ax)
a.ax.tick_params(labelsize=15)
a.set_label(r'Higher timescales',size=15)