#Preambule
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.tsa.stattools as stat
import matplotlib
from numpy.linalg import inv
matplotlib.style.use('ggplot')

#%% Exercise A
#Create delta function
def delta(t,t0):
    if t==t0:
        return 1
    if t!=t0:
        return 0
        
deltavec=[]
timevec=np.linspace(0, 600000,601)
for i in timevec:
    deltavec.append(delta(i,300000))

readvec=deltavec
freqvec=np.linspace(0,0.00005,101)

#%% Exercise B
#Create sine-wave function
sinevec=[]
timevec=np.linspace(0, 1000000,1001)
for i in timevec:
    sinevec.append(np.sin(i*2*np.pi/100000.))

readvec=sinevec
freqvec=np.linspace(0,0.00005,101)

#%% Exercise C
#Create saw tooth function
sawvec=[]
timevec=np.linspace(0,1000000,1001)
for i in timevec:
    sawvec.append()

#%% All
#Make discrete fourier transform
def Fourier(f,vector,tvec,dt):
    summation=[]
    for i in range(0,len(vector)-1):
        t=(tvec[i]+tvec[i+1])/2.
        summation.append((vector[i]+vector[i+1])*np.exp(2*np.pi*1j*f*t)*dt)
    return np.abs(np.sum(summation)**2)

#Retrieve data fourier
Fouriervec=[]
for i in freqvec:
    Fouriervec.append(Fourier(i,readvec,timevec,1000))

plt.figure(num=None, figsize=(7,3),dpi=150, facecolor='w', edgecolor='k')
plt.plot(freqvec,Fouriervec, 'r-',linewidth=3)
plt.ylabel('Power',fontsize=15)
plt.xlabel('Frequency',fontsize=15)
plt.tick_params(axis='both', which='major', labelsize=15)