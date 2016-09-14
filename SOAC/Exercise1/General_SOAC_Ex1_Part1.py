#Preambule
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.tsa.stattools as stat
import matplotlib
from numpy.linalg import inv
matplotlib.style.use('ggplot')

#Constants
tmax=3600.*24.
u0=0.
v0=0.
dt=1.
omega=7.2921*10**(-5)
lat=50.
f=2*omega*np.sin(lat/360.*2.*np.pi)
A=0.001 # amplitude in pressure variation per dx
B=0.
R = 	287.058 #gas constant
def rho(p,T): # p in hPa
    return p/(R*T)*100
rhoc= 1.225#density at 288 K, sea level
phi=0#-60./360.*2.*np.pi
c1=-A*f/(rhoc*(f**2-omega**2))
c2=0


#Vectors
vvec=np.zeros(np.int(tmax/dt))
uvec=np.zeros(np.int(tmax/dt))
tvec=np.zeros(np.int(tmax/dt))

#%%Calculations
for t in range(0,np.int(tmax/dt)):
    pgrady=0.
    pgradx=A*np.cos(omega*t+phi)+B
    
    vg=0#1/(rhoc*f)*pgradx
    ug=0#-1./(rhoc*f)*pgrady
    
    vvec[t]=vvec[t-1]+(-f*(uvec[t-1]-ug))*dt
    uvec[t]=uvec[t-1]+(f*(vvec[t]-vg)-pgradx/rhoc)*dt
    tvec[t]=t
   
#%%Analytical
uanalyt=np.zeros(np.int(tmax/dt))
vanalyt=np.zeros(np.int(tmax/dt))
for t in range(0,np.int(tmax/dt)):
    uanalyt[t]=c1*np.sin(f*t)+c2*np.cos(f*t)+A*omega/(rhoc*(f**2-omega**2))*np.sin(omega*t+phi)
    vanalyt[t]=c1*np.cos(f*t)+f*A/(rhoc*(f**2-omega**2))*np.cos(omega*t)

#%%Errors
Eu=sum((np.array(uanalyt)-np.array(uvec))**2)
Ev=sum((np.array(vanalyt)-np.array(vvec))**2)
#%%Plots
plt.figure(num=None, figsize=(7,3),dpi=150, facecolor='w', edgecolor='k')
plt.plot(tvec,uvec, 'r-',linewidth=2)
plt.plot(tvec,uanalyt, 'r--',linewidth=2)
plt.ylabel(r'U [ms$^{-1}$]',fontsize=15)
plt.xlabel('Time [s]',fontsize=15)
plt.tick_params(axis='both', which='major', labelsize=10)

plt.figure(num=None, figsize=(7,3),dpi=150, facecolor='w', edgecolor='k')
plt.plot(tvec,vvec, 'b-',linewidth=2)
plt.plot(tvec,vanalyt, 'b--',linewidth=2)
plt.ylabel(r'V [ms$^{-1}$]',fontsize=15)
plt.xlabel('Time [s]',fontsize=15)
plt.tick_params(axis='both', which='major', labelsize=10)