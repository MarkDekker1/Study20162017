#Preambule
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.tsa.stattools as stat
import matplotlib
from numpy.linalg import inv
matplotlib.style.use('ggplot')

#Constants
alpha1=0.75
alpha2=0.0
length=100

#Create AR(2) data
ARdata=np.zeros(length)+2.
for i in range(2,length):
    ARdata[i]=alpha1*ARdata[i-1]+alpha2*ARdata[i-2]

#%%Create Autocorrelation function
ACfunction=np.zeros(length)
Mean=np.mean(ARdata)
for k in range(0,length):
    ACvector=np.zeros(length-k)
    for i in range(0,length-k):
        ACvector[i]=(ARdata[i]-Mean)*(ARdata[i+k]-Mean)
    
    ACfunction[k]=sum(ACvector)/np.var(ARdata)/(length-k)
ACfunction=ACfunction[1:]

#%%https://www.empiwifo.uni-freiburg.de/lehre-teaching-1/winter-term/dateien-financial-data-analysis/handout-pacf.pdf
SIZE=20
PhiMatrix=np.zeros(shape=(SIZE,SIZE))

PhiMatrix[0,0]=ACfunction[0]
PhiMatrix[1,1]=(ACfunction[1]-(ACfunction[0])**2)/(1-(ACfunction[0])**2)
PhiMatrix[1,0]=PhiMatrix[0,0]-PhiMatrix[1,1]*PhiMatrix[0,0]#(ACfunction[0]-ACfunction[1]*ACfunction[0])/(1-PhiMatrix[1,1]*ACfunction[0])
PhiMatrix[2,2]=(ACfunction[2]-PhiMatrix[1,0]*ACfunction[1]-PhiMatrix[1,1]*ACfunction[0])/(1-PhiMatrix[1,0]*ACfunction[1]-PhiMatrix[1,1]*ACfunction[0])

for k in range(2,SIZE):
    
    if k>=3:
        Sumvec1=[]
        Sumvec2=[]
        for r in range(0,k):
            Sumvec1.append(PhiMatrix[k-1,r])
            Sumvec2.append(ACfunction[k-r])    
        PhiMatrix[k,k]=(ACfunction[k]-np.dot(Sumvec1,Sumvec2))/(1-np.dot(Sumvec1,Sumvec2))
    
    for j in range(0,k):
        PhiMatrix[k,j]=PhiMatrix[k-1,j]-PhiMatrix[k,k]*PhiMatrix[k-1,k-j-1]
        
#%%Plot data
plt.figure(num=None, figsize=(5,4),dpi=150, facecolor='w', edgecolor='k')
plt.plot(ARdata, 'k-',linewidth=3)
plt.ylabel('Data',fontsize=20)
plt.xlabel('Time',fontsize=20)
plt.tick_params(axis='both', which='major', labelsize=20)

#Plot autocorrelation function
plt.figure(num=None, figsize=(5,4),dpi=150, facecolor='w', edgecolor='k')
plt.plot(ACfunction, 'k-',linewidth=3)
plt.ylabel('ACF',fontsize=20)
plt.xlabel('Time lag',fontsize=20)
plt.xlim([0,SIZE])
plt.tick_params(axis='both', which='major', labelsize=20)

#Plot partial autocorrelation function
plt.figure(num=None, figsize=(5,4),dpi=150, facecolor='w', edgecolor='k')
plt.plot(np.diag(PhiMatrix), 'k-',linewidth=3)
plt.ylabel('PACF',fontsize=20)
plt.xlabel('Time lag',fontsize=20)
plt.xlim([0,SIZE])
plt.tick_params(axis='both', which='major', labelsize=20)