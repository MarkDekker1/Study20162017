#Preambule
import numpy as np
import matplotlib.pyplot as plt
import pandas
import statsmodels.tsa.stattools as stat
import matplotlib
matplotlib.style.use('ggplot')

#Reading data
f = open('C:\Users\Mark\Documents\Studie\Study20162017\MAIO\Data\Ex1_Data1.txt', 'r')
ARdata=[]
for line in f:
    ARdata.append(float(line))
length=len(ARdata)

#Autocorrelation function
ACfunction=np.zeros(length)
Mean=np.mean(ARdata)
for k in range(0,length):
    ACvector=np.zeros(length-k)
    for i in range(0,length-k):
        ACvector[i]=(ARdata[i]-Mean)*(ARdata[i+k]-Mean)
    
    ACfunction[k]=sum(ACvector)/np.var(ARdata)/(length-k)

#%% Partial autocorrelation function


#%%Plot data
plt.figure(num=None, figsize=(10,4),dpi=150, facecolor='w', edgecolor='k')
plt.plot(ARdata, 'k-',linewidth=2)
plt.ylabel('AR(2) data',fontsize=20)
plt.xlabel('Time',fontsize=20)
plt.tick_params(axis='both', which='major', labelsize=20)

#Plot autocorrelation function
plt.figure(num=None, figsize=(10,4),dpi=150, facecolor='w', edgecolor='k')
plt.plot(ACfunction, 'k-',linewidth=2)
plt.ylabel('rho',fontsize=20)
plt.xlabel('Time lag',fontsize=20)
plt.ylim([-1,1])
plt.tick_params(axis='both', which='major', labelsize=20)