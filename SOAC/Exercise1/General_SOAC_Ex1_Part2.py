#Preambule
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.tsa.stattools as stat
import matplotlib
from numpy.linalg import inv
#matplotlib.style.use('ggplot')
import csv

import matplotlib.cm as cm

#Read data
f = open(r'C:\Users\Mark Dekker\Documents\Study20162017\SOAC\Exercise1\Data.csv', 'r')
data=[]
#for line in f:
#    data.append(line)


with open(r'C:\Users\Mark Dekker\Documents\Study20162017\SOAC\Exercise1\Data.csv', 'rt') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',')
    for line in spamreader:
        data.append(line)

timevec=np.zeros(len(data))
dayvec=np.zeros(len(data))
hourvec=np.zeros(len(data))
dpdxvec=np.zeros(len(data))
dpdyvec=np.zeros(len(data))
u0vec=np.zeros(len(data))
v0vec=np.zeros(len(data))
dpdxmvec=np.zeros(len(data))
u0mvec=np.zeros(len(data))
v0mvec=np.zeros(len(data))
for i in range(0,len(data)):
    timevec[i]=data[i][0]
    dayvec[i]=data[i][1]
    hourvec[i]=data[i][2]
    dpdxvec[i]=data[i][3]
    dpdyvec[i]=data[i][4]
    u0vec[i]=data[i][5]
    v0vec[i]=data[i][6]
    if i>23:
        dpdxmvec[i]=data[i][7]
        u0mvec[i]=data[i][8]
        v0mvec[i]=data[i][9]

timevec=timevec*3600.
dpdxvec=dpdxvec/1000.
dpdyvec=dpdyvec/1000.
dpdxmvec=dpdxmvec/1000.

#%%Constants
tmax=172800.
u0=5.
v0=3.
dt=1
omega=7.2921*10**(-5)
lat=50.
f=2*omega*np.sin(lat/360.*2.*np.pi)
B=0.
R = 	287.058 #gas constant
def rho(p,T): # p in hPa
    return p/(R*T)*100.
rhoc= 1.225#density at 288 K, sea level
c1=-A*f/(rhoc*(f**2-omega**2))
c2=0
lda=0.0001


#Vectors
vvec_nog=np.zeros(np.int(tmax/dt))
uvec_nog=np.zeros(np.int(tmax/dt))
vvec_nol=np.zeros(np.int(tmax/dt))
uvec_nol=np.zeros(np.int(tmax/dt))
vvec_all=np.zeros(np.int(tmax/dt))
uvec_all=np.zeros(np.int(tmax/dt))
tvec=np.zeros(np.int(tmax/dt))

#initializing
vvec_all[0]=v0
vvec_nol[0]=v0
vvec_nog[0]=v0
uvec_all[0]=u0
uvec_nol[0]=u0
uvec_nog[0]=u0



#%%Calculations

tvec=np.zeros(np.int(tmax/dt))
for t in range(1,np.int(tmax/dt)):
    pgrady=0#M*np.cos(omega*t+theta/360.*2.*np.pi)
    pgradx=A*np.cos(omega*t+phi/360.*2.*np.pi)+B
    
    vg=1/(rhoc*f)*pgradx
    ug=-1./(rhoc*f)*pgrady
    
    vvec_nog[t]=vvec_nog[t-1]+(-f*(uvec_nog[t-1]-0))*dt
    uvec_nog[t]=uvec_nog[t-1]+(f*(vvec_nog[t]-0)-pgradx/rhoc)*dt
    
    vvec_nol[t]=vvec_nol[t-1]+(-f*(uvec_nol[t-1]-ug))*dt
    uvec_nol[t]=uvec_nol[t-1]+(f*(vvec_nol[t]-vg)-pgradx/rhoc)*dt
    
    vvec_all[t]=vvec_all[t-1]+(-f*(uvec_all[t-1]-ug)-lda*vvec_all[t-1])*dt
    uvec_all[t]=uvec_all[t-1]+(f*(vvec_all[t]-vg)-pgradx/rhoc-lda*uvec_all[t-1])*dt
    tvec[t]=t
   

#%% Take daily mean
umean=(uvec_all[0:86400]+uvec_all[86400:172800])/2.
vmean=(vvec_all[0:86400]+vvec_all[86400:172800])/2.
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
plt.figure(num=None, figsize=(10,7),dpi=150, facecolor='w', edgecolor='k')
plt.plot(tvec,uvec_nog, 'r-',linewidth=2)
plt.plot(tvec,uvec_nol, 'k-',linewidth=2)
plt.plot(tvec,uvec_all, 'b-',linewidth=2)
plt.plot(timevec,u0mvec, 'r--',linewidth=2)
plt.ylabel(r'U [ms$^{-1}$]',fontsize=15)
plt.xlabel('Time [s]',fontsize=15)
plt.xlim([82800,172800])
plt.tick_params(axis='both', which='major', labelsize=10)
plt.legend(['No geostrophic, no friction','no friction', 'all','measurements'])

plt.figure(num=None, figsize=(10,7),dpi=150, facecolor='w', edgecolor='k')
plt.plot(tvec,vvec_nog, 'r-',linewidth=2)
plt.plot(tvec,vvec_nol, 'k-',linewidth=2)
plt.plot(tvec,vvec_all, 'b-',linewidth=2)
plt.plot(timevec,v0mvec, 'r--',linewidth=2)
plt.ylabel(r'V [ms$^{-1}$]',fontsize=15)
plt.xlabel('Time [s]',fontsize=15)
plt.xlim([82800,172800])
plt.tick_params(axis='both', which='major', labelsize=10)
plt.legend(['No geostrophic, no friction','no friction', 'all','measurements'])