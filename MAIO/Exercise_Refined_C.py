#Preambule
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.tsa.stattools as stat
import matplotlib
from numpy.linalg import inv
matplotlib.style.use('ggplot')

#Constants
f = open('C:/Users/Mark Dekker/Documents/Study20162017/MAIO/Data/Ex1_Data1.txt', 'r')
ARdata=[]
for line in f:
    ARdata.append(float(line))
length=len(ARdata)
SIZE=30

#Remove linear trend
ARdataRef=[]
for i in range(0,length):
    ARdataRef.append(ARdata[i]-i/10000.)

#Create Autocorrelation function
ACF=stat.acf(ARdata)
PACF=stat.pacf(ARdata)
length2=len(ACF)

#%% Calculations
#%%MA(1)
beta1=(-1+np.sqrt(1-4*ACF[1]**2))/(2*ACF[1])

#%%MA(2)
from sympy.solvers import solve
from sympy import Symbol
x = Symbol('x')
beta1vec=solve(ACF[2]+x*ACF[2]/(ACF[1]+x*ACF[2])/(1.+x**2.+x**2.*(ACF[2])**2/(ACF[1]+x*ACF[2])**2.),x)
beta1=beta1vec[2]
beta2=beta1*ACF[2]/(ACF[1]+beta1*ACF[2])

#%%AR(1)
alpha1=ACF[1]

#%%AR(2)
alpha1=(ACF[2]/ACF[1]-1/ACF[1])/(1-(1/ACF[1])**2)
alpha2=1-alpha1/ACF[1]

#%%AR(1): Calculations
DIF=1
MatrixFITp=[]
MatrixFITa=[]

for k in range(0,1):
    alpha1=-0.1
    ADIFvec=[]
    PDIFvec=[]
    alphavec=[]
    for j in range(0,220):
        alpha1=alpha1+0.005
        
        FIT=np.zeros(length)+1.
        for i in range(1,length):
            FIT[i]=ARdata[i]-alpha1*ARdata[i-1]#+alpha2*ARdata[i-2]  
        
        ACFDIF=np.dot(stat.acf(FIT),stat.acf(FIT))
        PACFDIF=np.dot(stat.pacf(FIT),stat.pacf(FIT))
        ADIFvec.append(ACFDIF)
        PDIFvec.append(PACFDIF)
        alphavec.append(alpha1)
    MatrixFITp.append(ADIFvec)
    MatrixFITa.append(PDIFvec)
    print(k)

#%%AR(1): RMSE analysis
Vectora=[]
Vectorp=[]
for i in range(0,220):
    meanvectora=[]
    meanvectorp=[]
    for j in range(0,len(MatrixFITa)):
        meanvectora.append(MatrixFITa[j][i])
        meanvectorp.append(MatrixFITp[j][i])
    Vectora.append(np.mean(meanvectora))
    Vectorp.append(np.mean(meanvectorp))
    
Vectora=np.array(Vectora)
Vectorp=np.array(Vectorp)
Vector=Vectora+Vectorp
Minalpha=alphavec[np.where(Vector==np.min(Vector))[0]]

plt.figure(num=None, figsize=(10,3),dpi=150, facecolor='w', edgecolor='k')
plt.plot(alphavec,Vectora, 'k-',linewidth=3)
plt.plot(alphavec,Vectorp, 'r-',linewidth=3)
plt.plot(alphavec,Vectorp+Vectora, 'g-',linewidth=3)
plt.ylabel('S',fontsize=20)
plt.xlabel('Alpha_1',fontsize=20)
plt.tick_params(axis='both', which='major', labelsize=20)

FIT=np.zeros(length)+1.
for i in range(1,len(ARdata)):
    FIT[i]=ARdata[i]-Minalpha*ARdata[i-1]

plt.figure(num=None, figsize=(10,3),dpi=150, facecolor='w', edgecolor='k')
plt.plot(FIT, 'k-',linewidth=3)
plt.plot(ARdata, 'r-',linewidth=3)
plt.ylabel('Data',fontsize=20)
plt.xlabel('Time',fontsize=20)
plt.tick_params(axis='both', which='major', labelsize=20)

#%% AR(2): Calculations
alpha1=(ACF[2]/ACF[1]-1/ACF[1])/(1-(1/ACF[1])**2)
alpha2=1-alpha1/ACF[1]
FIT=np.zeros(length)+1

for i in range(2,length):
    FIT[i]=ARdata[i]-alpha1*ARdata[i-1]-alpha2*ARdata[i-2]
    
    
plt.figure(num=None, figsize=(10,3),dpi=150, facecolor='w', edgecolor='k')
plt.plot(stat.acf(ARdata), 'k-',linewidth=3)
plt.plot(stat.acf(FIT), 'b-',linewidth=3)
plt.ylabel('FIT',fontsize=20)
plt.xlabel('Timelag',fontsize=20)
plt.tick_params(axis='both', which='major', labelsize=20)    


#%% MA(2): Calculations
DIF=1
ARdata2=ARdata#-np.mean(ARdata)+1
MatrixFIT=[]
Parvec=[]

for k in range(0,1):
    beta1=0.2
    betavec=[]
    Difmat=[]
    for j in range(0,40):
        beta1=beta1+0.01
        
        beta2=0.4
        DIFvec=[]
        for r in range(0,40):
            beta2=beta2+0.01
            
            shock=np.zeros(length)+1.
            shock[0]=ARdata[0]
            shock[1]=ARdata[1]
            for i in range(2,length):
                shock[i]=ARdata[i]+beta1*shock[i-1]+beta2*shock[i-2]
                
            DIF=np.dot(stat.acf(shock),stat.acf(shock))+np.dot(stat.pacf(shock),stat.pacf(shock))
            DIFvec.append(DIF)
            Parvec.append([beta1, beta2])
        MatrixFIT.append(DIFvec)
    print(k)
    

#%%MA(2): RMSE analysis

Totallist=[]
for i in range(0,40):
    for j in range(0,40):
        Totallist.append(MatrixFIT[i][j])

Minvector=np.where(Totallist==np.nanmin(Totallist))[0]
Minindex=Minvector[0]

Minbeta=[(Minindex-np.mod(Minindex,40))/40.*0.01+0.2,np.mod(Minindex,40)*0.01+0.4]

FIT=np.zeros(length)+1.
FIT[0]=ARdata[0]
FIT[1]=ARdata[1]
for i in range(2,length):
    FIT[i]=ARdata[i]+Minbeta[0]*FIT[i-1]+Minbeta[1]*FIT[i-2]

plt.figure(num=None, figsize=(10,3),dpi=150, facecolor='w', edgecolor='k')
plt.plot(FIT, 'k-',linewidth=3)
plt.plot(ARdata2, 'r-',linewidth=3)
plt.ylabel('Data',fontsize=20)
plt.xlabel('Time',fontsize=20)
plt.tick_params(axis='both', which='major', labelsize=20)


#%% MA(1): Calculations
DIF=1
MatrixFIT=[]

for k in range(0,1):
    beta1=0
    DIFvec=[]
    betavec=[]
    for j in range(0,200):
        beta1=beta1+0.005
        
        shock=np.zeros(length)+1.
        shock[0]=ARdata[0]
        for i in range(1,length):
            shock[i]=ARdata[i]+beta1*shock[i-1]
            
        DIF=np.dot(stat.acf(shock),stat.acf(shock))+np.dot(stat.pacf(shock),stat.pacf(shock))
        DIFvec.append(DIF)
        betavec.append(beta1)
    MatrixFIT.append(DIFvec)
    print(k)
#%%MA(1): RMSE analysis
Vector=[]
for i in range(0,200):
    meanvector=[]
    for j in range(0,len(MatrixFIT)):
        meanvector.append(MatrixFIT[j][i])
    Vector.append(np.mean(meanvector))
    
Vector=np.array(Vector)
Minbeta=betavec[np.where(Vector==np.min(Vector))[0][0]]

plt.figure(num=None, figsize=(10,3),dpi=150, facecolor='w', edgecolor='k')
plt.plot(betavec,Vector, 'k-',linewidth=3)
plt.ylabel('RMSE',fontsize=20)
plt.xlabel('Beta_1',fontsize=20)
plt.tick_params(axis='both', which='major', labelsize=20)


FIT=np.zeros(length)+1.
FIT[0]=ARdata[0]
for i in range(1,length):
    FIT[i]=ARdata[i]+Minbeta*FIT[i-1]


plt.figure(num=None, figsize=(10,3),dpi=150, facecolor='w', edgecolor='k')
plt.plot(FIT, 'k-',linewidth=3)
plt.plot(ARdata2, 'r-',linewidth=3)
plt.ylabel('Data',fontsize=20)
plt.xlabel('Time',fontsize=20)
plt.tick_params(axis='both', which='major', labelsize=20)

