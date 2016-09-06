#Preambule
import numpy as np
import matplotlib.pyplot as plt
import pandas

f = open('Data\Ex1_Data1.txt', 'r')

ARdata=[]
for line in f:
    ARdata.append(float(line))
    
length=len(ARdata)

ACfunction=np.zeros(length)
Mean=np.mean(ARdata)
for k in range(0,length):
    ACvector=np.zeros(length-k)
    for i in range(k,length-k):
        ACvector[i]=(ARdata[i]-Mean)*(ARdata[i-k]-Mean)
    
    ACfunction[k]=sum(ACvector[0:(length-k)])/np.var(ARdata)


#%%Plot data
plt.figure(num=None, figsize=(10,4),dpi=150, facecolor='w', edgecolor='k')
plt.plot(ARdata, 'k-',linewidth=2)
plt.ylabel('AR(2) data',fontsize=20)
plt.xlabel('Time',fontsize=20)
plt.tick_params(axis='both', which='major', labelsize=20)

#Plot autocorrelation function
plt.figure(num=None, figsize=(10,4),dpi=150, facecolor='w', edgecolor='k')
plt.plot(ACfunction, 'k-',linewidth=2)
plt.ylabel('Rho',fontsize=20)
plt.xlabel('Time lag',fontsize=20)
plt.tick_params(axis='both', which='major', labelsize=20)