#Preambule
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.tsa.stattools as stat
import matplotlib
from numpy.linalg import inv
matplotlib.style.use('ggplot')

#Constants
alpha1=0.75
alpha2=-0.3
length=100

#Create AR(2) data
ARdata=np.zeros(length)+1.
for i in range(2,length):
    ARdata[i]=alpha1*ARdata[i-1]+alpha2*ARdata[i-2]

#Create Autocorrelation function
ACfunction=np.zeros(length)
Mean=np.mean(ARdata)
for k in range(0,length):
    ACvector=np.zeros(length-k)
    for i in range(0,length-k):
        ACvector[i]=(ARdata[i]-Mean)*(ARdata[i+k]-Mean)
    
    ACfunction[k]=sum(ACvector)/np.var(ARdata)/(length-k)

#%%Create Partial Autocorrelation function
#http://stats.stackexchange.com/questions/129052/acf-and-pacf-formula
L0=ARdata[0:(length-3)]
L1=ARdata[1:(length-2)]
L2=ARdata[2:(length-1)]

rho12=(length*np.dot(L0,L1)-sum(L0)*sum(L1))/np.sqrt((length*np.dot(L0,L0)-(sum(L1))**2)*(length*np.dot(L0,L0)-(sum(L1))**2))
rho23=(length*np.dot(L1,L2)-sum(L1)*sum(L2))/np.sqrt((length*np.dot(L1,L1)-(sum(L2))**2)*(length*np.dot(L1,L1)-(sum(L2))**2))
rho13=(length*np.dot(L0,L2)-sum(L0)*sum(L2))/np.sqrt((length*np.dot(L0,L0)-(sum(L2))**2)*(length*np.dot(L0,L0)-(sum(L2))**2))

rho13_2=(rho13-rho12*rho23)/np.sqrt((1-rho12**2)*(1-rho13**2))

#%% say up to k=4
Phivector=np.zeros(20)
for k in range(3,20):
    
    Kmax=k
    Matrix=np.zeros(shape=(Kmax,Kmax))
    for i in range(0,Kmax):
        for j in range(0,Kmax):
            for m in range(0,Kmax):
                if np.abs(i-j)==m:
                    Matrix[i,j]=ARdata[m]
    
    InvMatrix=inv(Matrix)
    Kvec=np.dot(InvMatrix,ARdata[1:(Kmax+1)])
    Phivector[k]= Kvec[k-1]


#%%
SIZE=20
PhiMatrix=np.zeros(shape=(SIZE,SIZE))

PhiMatrix[0,0]=ACfunction[0]
PhiMatrix[1,1]=(ACfunction[1]-(ACfunction[0])**2)/(1-(ACfunction[0])**2)
for k in range(1,SIZE):

    for j in range(0,k):
        print(j)
        PhiMatrix[k,j]=PhiMatrix[k-1,j]-PhiMatrix[k,k]*PhiMatrix[k-1,k-j]
        
    if k>=2:
        Sumvec1=[]
        Sum1vec2=[] 
        Sum2vec2=[]  
          
        for j in range(0,k-1):
            Sumvec1.append(PhiMatrix[k-1,j])
            Sum1vec2.append(ACfunction[k-j])
            Sum2vec2.append(ACfunction[j])
            
        PhiMatrix[k,k]=(ACfunction[k]-np.dot(Sumvec1,Sum1vec2))/(1-np.dot(Sumvec1,Sum2vec2))

plt.plot(np.diag(PhiMatrix))

#%%Plot data
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
plt.xlim([0,len(ARdata)/3])
plt.tick_params(axis='both', which='major', labelsize=20)