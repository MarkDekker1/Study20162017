import time
start_time = time.time()

Cmatrix_euler=np.zeros(shape=(2,np.int(L/Dx)))
for j in range(0,J):
    Cmatrix_euler[0,j]=C[j]
    
plt.figure(num=None, figsize=(8,4),dpi=150, facecolor='w', edgecolor='k')
plt.plot(xvec,Cmatrix_euler[0], 'r-',linewidth=2)

for Dz in [1,10,100,1000]:
        
    
    Cmatrix_euler=np.zeros(shape=(np.int(tmax/Dz),np.int(L/Dx)))
    
    for j in range(0,J):
        Cmatrix_euler[0,j]=C[j]
        
    for t in range(1,np.int(tmax/Dz)):
        for j in range(0,np.int(xmax/Dx)):
            Cmatrix_euler[t,j]=Cmatrix_euler[t-1,j]-u0*(Cmatrix_euler[t-1,j]-Cmatrix_euler[t-1,j-1])*Dz/Dx
            
    if Dz==1:
        plt.plot(xvec,Cmatrix_euler[np.int(tmax/Dz)-1], 'm-',linewidth=2)    
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
plt.legend(['Start', r'$\Delta$t=1', r'$\Delta$t=10', r'$\Delta$t=100', r'$\Delta$t=1000'])
plt.ylim([-0.2,1.2])

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
    y = Cmatrix_euler[i]
    line.set_data(x, y)
    return line,

# call the animator.  blit=True means only re-draw the parts that have changed.
anim = animation.FuncAnimation(fig, animate, init_func=init,
                               frames=25000, interval=0.01, blit=True)

#anim.save('basic_animation.mp4', fps=30, extra_args=['-vcodec', 'libx264'])

plt.show()