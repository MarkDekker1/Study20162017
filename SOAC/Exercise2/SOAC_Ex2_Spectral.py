import time
start_time = time.time()

Cmatrix_spec=np.zeros(shape=(tmax/Dt,L/Dx))

for j in range(0,J):
    Cmatrix_spec[0,j]=C[j]

#Transformation to spectral space
alpha=np.zeros(shape=(tmax/Dt,L/Dx))
beta=np.zeros(shape=(tmax/Dt,L/Dx))


for i in range(0,np.int(J/2.)):
    wavenumber=i
    summation=np.zeros(L/Dx)
    for j in range(0,J):
        summation[j]=C[j]*np.cos(-2*np.pi*wavenumber*j/J)
        
    alpha[0,i]=2./J*np.sum(summation)
    beta[0,i]=C[j]

#Time integration of coefficients
for t in range(1,tmax/Dt):
    Dummy1=np.zeros(xmax/Dx)
    Dummy2=np.zeros(xmax/Dx)
    for k in range(0,np.int(J/2.)):
        Dummy1[k]=alpha[t-1,k]+Dt*2.*np.pi*u0*k*beta[t-1,k]/L
        Dummy2[k]=beta[t-1,k]-Dt*2.*np.pi*u0*k*alpha[t-1,k]/L
        
    for k in range(0,np.int(J/2.)):
        alpha[t,k]=alpha[t-1,k]+Dt*2.*np.pi*u0*k*Dummy2[k]/L
        beta[t,k]=beta[t-1,k]-Dt*2.*np.pi*u0*k*Dummy1[k]/L
        
#Transformation back to physical space
Cmatrix_spec_sspace=np.array(alpha)+1j*np.array(beta)

for t in range(1,tmax/Dt):
    for i in range(0,L/Dx):
        summation=np.zeros(np.int(J/2.))
        for k in range(0,np.int(J/2.)):
            summation[k]=Cmatrix_spec_sspace[t,k]*np.exp(1j*(2.*np.pi*k*i*Dx/L))
        Cmatrix_spec[t,i]=np.real(sum(summation))
            
print("--- %s seconds ---" % (time.time() - start_time))

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
                               frames=25000, interval=0.1, blit=True)

#anim.save('basic_animation.mp4', fps=30, extra_args=['-vcodec', 'libx264'])

plt.show()