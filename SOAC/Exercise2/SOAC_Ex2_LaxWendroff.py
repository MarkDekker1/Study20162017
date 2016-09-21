import time
start_time = time.time()

Cmatrix_laxw=np.zeros(shape=(np.int(tmax/Dt),np.int(L/Dx)))

for j in range(0,J):
    Cmatrix_laxw[0,j]=C[j]
    
for t in range(1,np.int(tmax/Dt)):
    for j in range(0,np.int(xmax/Dx)):
        if j!=np.int(xmax/Dx)-1:
            Cmatrix_laxw[t,j]=Cmatrix_laxw[t-1,j]+(-u0*(Cmatrix_laxw[t-1,j+1]-Cmatrix_laxw[t-1,j-1])/(2*Dx)+u0**2.*Dt/2.*(Cmatrix_laxw[t-1,j+1]-2.*Cmatrix_laxw[t-1,j]+Cmatrix_laxw[t-1,j-1])/(Dx**2))*Dt
        if j==np.int(xmax/Dx)-1:
            Cmatrix_laxw[t,j]=Cmatrix_laxw[t-1,j]+(-u0*(Cmatrix_laxw[t-1,0]-Cmatrix_laxw[t-1,j-1])/(2*Dx)+u0**2.*Dt/2.*(Cmatrix_laxw[t-1,0]-2.*Cmatrix_laxw[t-1,j]+Cmatrix_laxw[t-1,j-1])/(Dx**2))*Dt
        
    
            
print("--- %s seconds ---" % (time.time() - start_time))

plt.figure(num=None, figsize=(10,7),dpi=150, facecolor='w', edgecolor='k')
plt.plot(xvec,Cmatrix_laxw[0], 'r-',linewidth=2)
plt.plot(xvec,Cmatrix_laxw[tmax/Dt-1], 'k-',linewidth=2)
plt.ylabel(r'Concentration',fontsize=15)
plt.xlabel('Distance [m]',fontsize=15)
plt.tick_params(axis='both', which='major', labelsize=10)
plt.ylim([-0.2,1.2])
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
    y = Cmatrix_laxw[i]
    line.set_data(x, y)
    return line,

# call the animator.  blit=True means only re-draw the parts that have changed.
anim = animation.FuncAnimation(fig, animate, init_func=init,
                               frames=25000, interval=0.01, blit=True)

#anim.save('basic_animation.mp4', fps=30, extra_args=['-vcodec', 'libx264'])

plt.show()