#Preambule
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.tsa.stattools as stat
import matplotlib
matplotlib.style.use('ggplot')

#Constants
alpha1=0.75
alpha2=0.0
length=75

#Create AR(2) data
ARdata=np.zeros(length)+1.
for i in range(2,length):
    ARdata[i]=alpha1*ARdata[i-1]+alpha2*ARdata[i-2]+np.random.normal(0,10)

#Create Autocorrelation function
length=len(ARdata)

ACfunction=np.zeros(length)
Mean=np.mean(ARdata)
for k in range(0,length):
    ACvector=np.zeros(length-k)
    for i in range(0,length-k):
        ACvector[i]=(ARdata[i]-Mean)*(ARdata[i+k]-Mean)
    
    ACfunction[k]=sum(ACvector)/np.var(ARdata)/(length-k)

#Plot data
plt.figure(num=None, figsize=(5,4),dpi=150, facecolor='w', edgecolor='k')
plt.plot(ARdata, 'k-',linewidth=3)
plt.ylabel('AR(2) data',fontsize=20)
plt.xlabel('Time',fontsize=20)
plt.tick_params(axis='both', which='major', labelsize=20)

#Plot autocorrelation function
plt.figure(num=None, figsize=(5,4),dpi=150, facecolor='w', edgecolor='k')
plt.plot(ACfunction, 'k-',linewidth=3)
plt.ylabel('Rho',fontsize=20)
plt.xlabel('Time lag',fontsize=20)
plt.tick_params(axis='both', which='major', labelsize=20)