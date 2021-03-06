import time
start_time = time.time()

plt.figure(num=None, figsize=(8,4),dpi=150, facecolor='w', edgecolor='k')

tmax=250*1000
J=100
Cmatrix_spec=np.zeros(shape=(np.int(tmax/Dt),np.int(L/Dx)))

for j in range(0,J):
    Cmatrix_spec[0,j]=C[j]
plt.plot(xvec,Cmatrix_spec[0], 'r-',linewidth=2)

Dzvec=[10,100]

for Dz in Dzvec:
    Cmatrix_spec=np.zeros(shape=(np.int(tmax/Dz),np.int(L/Dx)))

    for j in range(0,J):
        Cmatrix_spec[0,j]=C[j]
    #Transformation to spectral space
    alpha=np.zeros(shape=(np.int(tmax/Dz),np.int(L/Dx)),dtype='f')
    beta=np.zeros(shape=(np.int(tmax/Dz),np.int(L/Dx)),dtype='f')
    
    
    for i in range(0,np.int(J/2.)):
        wavenumber=i
        summation1=np.zeros(np.int(L/Dx))
        summation2=np.zeros(np.int(L/Dx))
        for j in range(0,J):
            summation1[j]=C[j]*np.cos(-2.*np.pi*wavenumber*j/J)
            summation2[j]=C[j]*np.sin(-2.*np.pi*wavenumber*j/J)
            
        #alpha[0,i]=2./J*np.sum(summation)
        #beta[0,i]=C[j]
        alpha[0,i]=2./J*np.sum(summation1)
        beta[0,i]=2./J*np.sum(summation2)
    print('part 1 completed of Dz='+str(Dz))
    
    #Time integration of coefficients
    for t in range(1,np.int(tmax/Dz)):
        Dummy1=np.zeros(np.int(xmax/Dx),dtype='f')
        Dummy2=np.zeros(np.int(xmax/Dx),dtype='f')
        for k in range(0,np.int(J/2.)):
            Dummy1[k]=alpha[t-1,k]+Dz*2.*np.pi*u0*k*beta[t-1,k]/L
            Dummy2[k]=beta[t-1,k]-Dz*2.*np.pi*u0*k*alpha[t-1,k]/L
            
        for k in range(0,np.int(J/2.)):
            alpha[t,k]=alpha[t-1,k]+Dz*2.*np.pi*u0*k*Dummy2[k]/L
            beta[t,k]=beta[t-1,k]-Dz*2.*np.pi*u0*k*Dummy1[k]/L
    print('part 2 completed of Dz='+str(Dz))
            
    #Transformation back to physical space
    Cmatrix_spec_sspace=np.array(alpha)+1j*np.array(beta)
    
    for t in range(1,np.int(tmax/Dz)):
        for i in range(0,np.int(L/Dx)):
            summation=np.zeros(np.int(J/2.))
            for k in range(0,np.int(J/2.)):
                summation[k]=np.real(Cmatrix_spec_sspace[t,k]*np.exp(1j*(2.*np.pi*k*i*Dx/L)))
            Cmatrix_spec[t,i]=sum(summation)
    print('part 3 completed of Dz='+str(Dz))
    
    if Dz==10:
        plt.plot(xvec,Cmatrix_spec[np.int(tmax/Dz)-1]-np.mean(C), 'k-',linewidth=2)
    if Dz==100:
        plt.plot(xvec,Cmatrix_spec[np.int(tmax/Dz)-1]-np.mean(C), 'g-',linewidth=2)
    if Dz==1000:
        plt.plot(xvec,Cmatrix_spec[np.int(tmax/Dz)-1]-np.mean(C), 'b-',linewidth=2)
    print('part 4 completed of Dz='+str(Dz))
            
print("--- %s seconds ---" % (time.time() - start_time))

plt.ylabel(r'Concentration',fontsize=15)
plt.xlabel('Distance [m]',fontsize=15)
plt.tick_params(axis='both', which='major', labelsize=10)
plt.ylim([-0.2,1.2])
plt.legend(['Start', r'$\Delta$t=10', r'$\Delta$t=100'])

#%%
plt.figure(num=None, figsize=(10,5),dpi=150, facecolor='w', edgecolor='k')
plt.plot(xvec,Cmatrix_spec[0], 'r-',linewidth=2)
plt.plot(xvec,Cmatrix_spec[tmax/Dt-1], 'k-',linewidth=2)
plt.ylabel(r'Concentration',fontsize=15)
plt.xlabel('Distance [m]',fontsize=15)
plt.tick_params(axis='both', which='major', labelsize=10)
plt.legend(['Before', 'After'])

#%% Animation
from matplotlib import animation

# First set up the figure, the axis, and the plot element we want to animate
fig = plt.figure()
ax = plt.axes(xlim=(0, L), ylim=(-0.5,2))
line, = ax.plot([], [], lw=2)

# initialization function: plot the background of each frame
def init():
    line.set_data([], [])
    return line,

# animation function.  This is called sequentially
def animate(i):
    x = xvec
    y = Cmatrix_spec[i]
    line.set_data(x, y)
    return line,

# call the animator.  blit=True means only re-draw the parts that have changed.
anim = animation.FuncAnimation(fig, animate, init_func=init,
                               frames=250, interval=100, blit=True)

#anim.save('basic_animation.mp4', fps=30, extra_args=['-vcodec', 'libx264'])

plt.show()