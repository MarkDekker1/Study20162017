import time
start_time = time.time()

plt.figure(num=None, figsize=(8,4),dpi=150, facecolor='w', edgecolor='k')

for Dz in [1,10,100,1000]:
        
    
    Cmatrix_euler=np.zeros(shape=(np.int(tmax/Dz),np.int(L/Dx)))
    plt.plot(xvec,Cmatrix_euler[0], 'r-',linewidth=2)
    
    for j in range(0,J):
        Cmatrix_euler[0,j]=C[j]
        
    for t in range(1,np.int(tmax/Dz)):
        for j in range(0,np.int(xmax/Dx)):
            Cmatrix_euler[t,j]=Cmatrix_euler[t-1,j]-u0*(Cmatrix_euler[t-1,j]-Cmatrix_euler[t-1,j-1])*Dz/Dx
    
    if Dz==10:
        plt.plot(xvec,Cmatrix_euler[np.int(tmax/Dz)-1], 'k-',linewidth=2)
    if Dz==100:
        plt.plot(xvec,Cmatrix_euler[np.int(tmax/Dz)-1], 'g-',linewidth=2)
    if Dz==1000:
        plt.plot(xvec,Cmatrix_euler[np.int(tmax/Dz)-1], 'b-',linewidth=2)
            
print("--- %s seconds ---" % (time.time() - start_time))

plt.ylabel(r'Concentration',fontsize=15)
plt.xlabel('Distance [m]',fontsize=15)
plt.tick_params(axis='both', which='major', labelsize=10)
plt.legend(['Start', r'$\Delta$t=10', r'$\Delta$t=100', r'$\Delta$t=1000'])
plt.ylim([-0.2,1.2])