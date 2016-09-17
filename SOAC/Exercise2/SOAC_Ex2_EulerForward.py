import time
start_time = time.time()

Cmatrix_euler=np.zeros(shape=(tmax/Dt,L/Dx))

for j in range(0,J):
    Cmatrix_euler[0,j]=C[j]
    
for t in range(1,tmax/Dt):
    for j in range(0,xmax/Dx):
        Cmatrix_euler[t,j]=Cmatrix_euler[t-1,j]-u0*(Cmatrix_euler[t-1,j]-Cmatrix_euler[t-1,j-1])*Dt/Dx
            
print("--- %s seconds ---" % (time.time() - start_time))

plt.figure(num=None, figsize=(10,4),dpi=150, facecolor='w', edgecolor='k')
plt.plot(xvec,Cmatrix_euler[0], 'r-',linewidth=2)
plt.plot(xvec,Cmatrix_euler[tmax/Dt-1], 'k-',linewidth=2)
plt.ylabel(r'Concentration',fontsize=15)
plt.xlabel('Distance [m]',fontsize=15)
plt.tick_params(axis='both', which='major', labelsize=10)
plt.legend(['Before, After'])