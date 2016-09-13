#Preambule
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.tsa.stattools as stat
import matplotlib
from numpy.linalg import inv
matplotlib.style.use('ggplot')

#Constants
alpha1=0.7
alpha2=0.35
length=50
SIZE=30
noise=0
mu=0
var=1

#Create AR(2) data
ARdata=np.zeros(length)+1.
for i in range(2,length):
    ARdata[i]=alpha1*ARdata[i-1]+alpha2*ARdata[i-2]
    if noise==1:
        ARdata[i]=ARdata[i]+np.random.normal(mu,var)

#Create Autocorrelation function
ACF=stat.acf(ARdata)
PACF=stat.pacf(ARdata)

#Plot data
plt.figure(num=None, figsize=(5,4),dpi=150, facecolor='w', edgecolor='k')
plt.plot(ARdata, 'k-',linewidth=3)
plt.ylabel('Data',fontsize=20)
plt.xlabel('Time',fontsize=20)
plt.tick_params(axis='both', which='major', labelsize=20)

#Plot autocorrelation function
plt.figure(num=None, figsize=(5,4),dpi=150, facecolor='w', edgecolor='k')
plt.plot(ACF, 'k-',linewidth=3)
plt.ylabel('ACF',fontsize=20)
plt.xlabel('Time lag',fontsize=20)
plt.xlim([0,40])
plt.tick_params(axis='both', which='major', labelsize=20)

#Plot partial autocorrelation function
plt.figure(num=None, figsize=(5,4),dpi=150, facecolor='w', edgecolor='k')
plt.plot(PACF, 'k-',linewidth=3)
plt.ylabel('PACF',fontsize=20)
plt.xlabel('Time lag',fontsize=20)
plt.xlim([0,SIZE])
plt.tick_params(axis='both', which='major', labelsize=20)