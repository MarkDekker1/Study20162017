#Preambule
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.tsa.stattools as stat
import matplotlib
from numpy.linalg import inv
matplotlib.style.use('ggplot')
import csv
import matplotlib.cm as cm

#Constants
L=2500*1000
xmax=L
Dx=25*1000
J=100
C=np.zeros(100)
xvec=np.zeros(100)
C0=1
u0=10
tmax=250*1000
Dt=100

for j in range(0,J):
    x=j*Dx
    xvec[j]=x
    if x>=1125*1000 and x<=1375*1000:
        C[j]=C0

#%%
plt.figure(num=None, figsize=(10,5),dpi=150, facecolor='w', edgecolor='k')
plt.plot(xvec,Cmatrix_spec[0], 'r-',linewidth=2)
plt.plot(xvec,Cmatrix_euler[tmax/Dt-1], 'k-',linewidth=2)
plt.plot(xvec,Cmatrix_laxw[tmax/Dt-1], 'b-',linewidth=2)
plt.plot(xvec,Cmatrix_spec[tmax/Dt-1], 'm-',linewidth=2)
plt.ylabel(r'Concentration',fontsize=15)
plt.xlabel('Distance [m]',fontsize=15)
plt.tick_params(axis='both', which='major', labelsize=10)
plt.legend(['Start', 'Euler', 'Lax-Wendroff', 'Spectral'])
