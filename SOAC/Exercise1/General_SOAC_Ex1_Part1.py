#Preambule
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.tsa.stattools as stat
import matplotlib
from numpy.linalg import inv
matplotlib.style.use('ggplot')

#Constants
tmax=3600.*24.*20
u0=0.
v0=0.
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


dt=100

Euextra=[]
Evextra=[]
dtvector=[10]

plt.figure(num=None, figsize=(7,3),dpi=150, facecolor='w', edgecolor='k')

for dt in dtvector:
    
    
    #Vectors
    vvec=np.zeros(np.int(tmax/dt))
    uvec=np.zeros(np.int(tmax/dt))
    tvec=np.zeros(np.int(tmax/dt))
    
    #Calculations
    for i in range(0,np.int(tmax/dt)):
        pgrady=0.
        pgradx=A*np.cos(omega*i*dt+phi)+B
        
        vg=0#1/(rhoc*f)*pgradx
        ug=0#-1./(rhoc*f)*pgrady
        
        vvec[i]=vvec[i-1]+(-f*(uvec[i-1]-ug))*dt
        uvec[i]=uvec[i-1]+(f*(vvec[i]-vg)-pgradx/rhoc)*dt
        tvec[i]=i*dt
       
    #Analytical
    uanalyt=np.zeros(np.int(tmax/dt))
    vanalyt=np.zeros(np.int(tmax/dt))
    for i in range(0,np.int(tmax/dt)):
        t=i*dt
        uanalyt[i]=c1*np.sin(f*t)+c2*np.cos(f*t)+A*omega/(rhoc*(f**2-omega**2))*np.sin(omega*t+phi)
        vanalyt[i]=c1*np.cos(f*t)+f*A/(rhoc*(f**2-omega**2))*np.cos(omega*t)
    
    #Errors
    Eu=sum((np.array(uanalyt)-np.array(uvec))**2)
    Ev=sum((np.array(vanalyt)-np.array(vvec))**2)
    
    Euvec=(np.array(uanalyt)-np.array(uvec))
    Evvec=(np.array(vanalyt)-np.array(vvec))
    
    Euextra.append(Eu)
    Evextra.append(Ev)
    
    plt.plot(tvec/3600.,Euvec,linewidth=2)
    
plt.ylabel('RSME of U',fontsize=15)
plt.xlabel('Time [h]',fontsize=15)
plt.tick_params(axis='both', which='major', labelsize=10)
plt.legend([r'$\Delta$t=1 s','$\Delta$t=10 s','$\Delta$t=100 s','$\Delta$t=1000 s'],loc=4)


plt.figure(num=None, figsize=(7,3),dpi=150, facecolor='w', edgecolor='k')
plt.semilogy(dtvector,Euextra, 'r-',linewidth=2)
plt.semilogy(dtvector,Evextra, 'b-',linewidth=2)
plt.ylabel('RSME of U, V',fontsize=15)
plt.xlabel(r'$\Delta$t',fontsize=15)
plt.tick_params(axis='both', which='major', labelsize=10)

#%%Plots
plt.figure(num=None, figsize=(7,3),dpi=150, facecolor='w', edgecolor='k')
plt.plot(tvec/3600.,uvec, 'r-',linewidth=2)
plt.plot(tvec/3600.,uanalyt, 'r--',linewidth=2)
plt.ylabel(r'U [ms$^{-1}$]',fontsize=15)
plt.xlabel('Time [h]',fontsize=15)
plt.tick_params(axis='both', which='major', labelsize=10)

plt.figure(num=None, figsize=(7,3),dpi=150, facecolor='w', edgecolor='k')
plt.plot(tvec/3600.,vvec, 'b-',linewidth=2)
plt.plot(tvec/3600.,vanalyt, 'b--',linewidth=2)
plt.ylabel(r'V [ms$^{-1}$]',fontsize=15)
plt.xlabel('Time [h]',fontsize=15)
plt.tick_params(axis='both', which='major', labelsize=10)

plt.figure(num=None, figsize=(7,3),dpi=150, facecolor='w', edgecolor='k')
plt.plot(tvec/3600.,Euvec, 'r-',linewidth=2)
plt.plot(tvec/3600.,Evvec, 'b-',linewidth=2)
plt.ylabel('Error',fontsize=15)
plt.xlabel('Time [h]',fontsize=15)
plt.tick_params(axis='both', which='major', labelsize=10)

print('RSME in u: ',Eu)
print('RSME in v: ',Ev)

#%% Fourier of RSME

freqcheck=np.fft.fftfreq(len(Euvec),d=10)
fouriercheck=np.abs(np.fft.fft(Euvec))**2

#Check
plt.figure(num=None, figsize=(7,3),dpi=150, facecolor='w', edgecolor='k')
plt.plot(1/(freqcheck[8:500]*3600.),fouriercheck[8:500], 'r-',linewidth=3)
plt.ylabel('Power',fontsize=15)
plt.xlabel(r'Period [h]',fontsize=15)
plt.tick_params(axis='both', which='major', labelsize=15)
