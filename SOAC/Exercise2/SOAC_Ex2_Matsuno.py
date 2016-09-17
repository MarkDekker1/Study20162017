import time
start_time = time.time()

Cmatrix_mats=np.zeros(shape=(tmax/Dt,L/Dx))

for j in range(0,J):
    Cmatrix_mats[0,j]=C[j]

for t in range(1,tmax/Dt):
    Dummy=np.zeros(xmax/Dx)
    for j in range(0,xmax/Dx):
        Dummy[j]=Cmatrix_mats[t-1,j]-u0*(Cmatrix_mats[t-1,j]-Cmatrix_mats[t-1,j-1])*Dt/Dx
        
    for j in range(0,xmax/Dx):
        Cmatrix_mats[t,j]=Cmatrix_mats[t-1,j]-u0*(Dummy[j]-Dummy[j-1])*Dt/Dx
            
print("--- %s seconds ---" % (time.time() - start_time))

plt.figure(num=None, figsize=(10,7),dpi=150, facecolor='w', edgecolor='k')
plt.plot(xvec,Cmatrix_mats[0], 'r-',linewidth=2)
plt.plot(xvec,Cmatrix_mats[tmax/Dt-1], 'k-',linewidth=2)
plt.ylabel(r'Concentration',fontsize=15)
plt.xlabel('Distance [m]',fontsize=15)
plt.tick_params(axis='both', which='major', labelsize=10)
plt.legend(['Before', 'After'])