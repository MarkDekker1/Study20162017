#Preambule
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.tsa.stattools as stat
import matplotlib
from numpy.linalg import inv
matplotlib.style.use('ggplot')
import csv

#Read data
f = open('C:\Users\Mark\Documents\Studie\Study20162017\SOAC\Exercise1\Data.csv', 'r')
data=[]
#for line in f:
#    data.append(line)


with open('C:\Users\Mark\Documents\Studie\Study20162017\SOAC\Exercise1\Data.csv', 'rb') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',')
    for row in spamreader:
        data.append(row)

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

#%%Constants
tmax=169201.
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
    return p/(R*T)*100.
rhoc= 1.225#density at 288 K, sea level
phi=0#-60./360.*2.*np.pi
c1=-A*f/(rhoc*(f**2-omega**2))
c2=0


#Vectors
vvec=np.zeros(np.int(tmax/dt))
uvec=np.zeros(np.int(tmax/dt))
tvec=np.zeros(np.int(tmax/dt))

#%%Afschatten A
tvec=[]
for t in range(0,np.int(tmax/dt)):
    tvec.append(t)

Epvec=[]
for TryA in np.linspace(0,0.002,10):
    pgradx=[]
    for t in range(0,np.int(tmax/dt)):
        pgradx.append(A*np.cos(omega*t+phi))
    
    Epvec.append(np.sum((pgradx[0:169201:3600]-dpdxvec)**2))


plt.figure(num=None, figsize=(7,3),dpi=150, facecolor='w', edgecolor='k')
plt.plot(tvec,pgradx, 'b-',linewidth=2)
plt.plot(timevec,dpdxvec, 'b--',linewidth=2)
plt.ylabel(r'$\frac{\partial p}{\partial x}$ [hPa m$^{-1}$]',fontsize=15)
plt.xlabel('Time [s]',fontsize=15)
plt.tick_params(axis='both', which='major', labelsize=10)
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
#plt.plot(tvec,uanalyt, 'r--',linewidth=2)
plt.plot(timevec,u0vec, 'r--',linewidth=2)
plt.ylabel(r'U [ms$^{-1}$]',fontsize=15)
plt.xlabel('Time [s]',fontsize=15)
plt.tick_params(axis='both', which='major', labelsize=10)

plt.figure(num=None, figsize=(7,3),dpi=150, facecolor='w', edgecolor='k')
plt.plot(tvec,vvec, 'b-',linewidth=2)
plt.plot(tvec,vanalyt, 'b--',linewidth=2)
plt.ylabel(r'V [ms$^{-1}$]',fontsize=15)
plt.xlabel('Time [s]',fontsize=15)
plt.tick_params(axis='both', which='major', labelsize=10)