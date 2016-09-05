#Preambule
import numpy as np
import matplotlib.pyplot as plt

#Constants
alpha1=0.3
alpha2=0.9

#Create AR(2) data
ARdata=np.zeros(100)+1.
for i in range(2,100):
    ARdata[i]=alpha1*ARdata[i-1]+alpha2*ARdata[i-2]

#Create Autocorrelation function
ACfunction=np.zeros(100)
for k in range(0,100):
    ACvector=np.zeros(100-k)
    for i in range(0,100-k):
        ACvector[i]=(ARdata[i]-np.mean(ARdata))*(ARdata[i-k]-np.mean(ARdata))
    
    ACfunction[k]=sum(ACvector[0:(100-k)])/np.var(ARdata)

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