#%%Afschatten lambda

tvec=[]
for t in range(0,np.int(tmax/dt)):
    tvec.append(t*dt)


lambdavec=np.linspace(0.0001,0.0007,15)

Euvec=[]
Evvec=[]
ruvec=[]
rvvec=[]
for TryLambda in [0.0001]:
    pgradx=[]
    tvec=np.zeros(np.int(tmax/dt))
    vvec_all=np.zeros(np.int(tmax/dt))
    uvec_all=np.zeros(np.int(tmax/dt))
    vvec_all[0]=v0
    uvec_all[0]=u0
    for t in range(1,np.int(tmax/dt)):
        
        pgrady0=np.mean(dpdyvec)#M*np.cos(omega*t+theta/360.*2.*np.pi)
        pgradx=A*np.cos(omega*t+phi/360.*2.*np.pi)+B
        
        vg=1/(rhoc*f)*pgradx
        ug=-1./(rhoc*f)*pgrady0
    
        vvec_all[t]=vvec_all[t-1]+(-f*(uvec_all[t-1]-ug)-TryLambda*vvec_all[t-1])*dt
        uvec_all[t]=uvec_all[t-1]+(f*(vvec_all[t]-vg)-pgradx/rhoc-TryLambda*uvec_all[t-1])*dt
        tvec[t]=t
    
    Euvec.append(np.sum((uvec_all[0:172800:3600]-u0vec)**2))
    Evvec.append(np.sum((vvec_all[0:172800:3600]-v0vec)**2))
    ruvec.append(np.corrcoef(uvec_all[0:172800:3600],u0vec)[1][0])
    rvvec.append(np.corrcoef(vvec_all[0:172800:3600],v0vec)[1][0])
    print(TryLambda)

#%% Plot voor afschatten
Evec=(np.array(Euvec)+np.array(Evvec))/2.

plt.figure(num=None, figsize=(7,3),dpi=150, facecolor='w', edgecolor='k')
plt.plot(lambdavec,Euvec, 'r--',linewidth=2)
plt.plot(lambdavec,Evvec, 'b--',linewidth=2)
plt.plot(lambdavec,Evec, 'k-',linewidth=2)
plt.ylabel('Error',fontsize=15)
plt.xlabel(r'$\lambda$',fontsize=15)
plt.tick_params(axis='both', which='major', labelsize=10)

plt.figure(num=None, figsize=(7,3),dpi=150, facecolor='w', edgecolor='k')
plt.plot(lambdavec,ruvec, 'r--',linewidth=2)
plt.plot(lambdavec,rvvec, 'b--',linewidth=2)
plt.plot(lambdavec,(np.array(ruvec)+np.array(rvvec))/2., 'k-',linewidth=2)
plt.ylabel('Correlation coefficient',fontsize=15)
plt.xlabel(r'$\lambda$',fontsize=15)
plt.tick_params(axis='both', which='major', labelsize=10)

#find minima
lambdaindex=np.where(Evec==np.min(Evec))[0]


lda=lambdavec[lambdaindex]
#%%
pgradx=[]
pgrady=[]
vvec_all=np.zeros(np.int(tmax/dt))
uvec_all=np.zeros(np.int(tmax/dt))
vvec_all[0]=v0
uvec_all[0]=u0
for t in range(1,np.int(tmax/dt)):
    
    pgrady=0#M*np.cos(omega*t+theta/360.*2.*np.pi)
    pgradx=A*np.cos(omega*t+phi/360.*2.*np.pi)+B
    
    vg=1/(rhoc*f)*pgradx
    ug=-1./(rhoc*f)*pgrady

    vvec_all[t]=vvec_all[t-1]+(-f*(uvec_all[t-1]-ug)-lda*vvec_all[t-1])*dt
    uvec_all[t]=uvec_all[t-1]+(f*(vvec_all[t]-vg)-pgradx/rhoc-lda*uvec_all[t-1])*dt
    tvec[t]=t



#%%Afschatten v0,u0
v0veci=np.linspace(-5,2,10)
u0veci=np.linspace(-11,-6,10)

tvec=[]
for t in range(0,np.int(tmax/dt)):
    tvec.append(t*dt)

Eumatrix=[]
Evmatrix=[]
for Tryv0 in v0veci:
    
    Euvec=[]
    Evvec=[]
    for Tryu0 in u0veci:
        pgradx=[]
        tvec=np.zeros(np.int(tmax/dt))
        vvec_all=np.zeros(np.int(tmax/dt))
        uvec_all=np.zeros(np.int(tmax/dt))
        vvec_all[0]=Tryv0
        uvec_all[0]=Tryu0
        for t in range(1,np.int(tmax/dt)):
            
            pgrady=0#M*np.cos(omega*t+theta/360.*2.*np.pi)
            pgradx=A*np.cos(omega*t+phi/360.*2.*np.pi)+B
            
            vg=1/(rhoc*f)*pgradx
            ug=-1./(rhoc*f)*pgrady
        
            vvec_all[t]=vvec_all[t-1]+(-f*(uvec_all[t-1]-ug)-TryLambda*vvec_all[t-1])*dt
            uvec_all[t]=uvec_all[t-1]+(f*(vvec_all[t]-vg)-pgradx/rhoc-TryLambda*uvec_all[t-1])*dt
            tvec[t]=t
        
        Euvec.append(np.sum((uvec_all[0:172800:3600]-u0vec)**2))
        Evvec.append(np.sum((vvec_all[0:172800:3600]-v0vec)**2))
    Eumatrix.append(Euvec)
    Evmatrix.append(Evvec)
    print(Tryv0)


#%% Plot voor afschatten
Ematrix=np.array(Eumatrix)+np.array(Evmatrix)

plt.figure(num=None, figsize=(7, 4), dpi=100, facecolor='w', edgecolor='k')
cs=plt.contourf(u0veci,v0veci,Ematrix,100,cmap=cm.coolwarm)
plt.contour(u0veci,v0veci,Ematrix,15,linewidth=3.0,colors='k')
cbar = plt.colorbar(cs)
plt.ylabel(r'V [m s$^{-1}$]',fontsize=15)
plt.xlabel(r'U [m s$^{-1}$]',fontsize=15)
plt.tick_params(axis='both', which='major', labelsize=10)


#find minima
vindex=np.where(Ematrix==np.min(Ematrix))[0]
uindex=np.where(Ematrix==np.min(Ematrix))[1]


u0=u0veci[uindex]
v0=v0veci[vindex]

pgradx=[]
pgrady=[]
vvec_all=np.zeros(np.int(tmax/dt))
uvec_all=np.zeros(np.int(tmax/dt))
vvec_all[0]=v0
uvec_all[0]=u0
for t in range(1,np.int(tmax/dt)):
    
    pgrady=0#M*np.cos(omega*t+theta/360.*2.*np.pi)
    pgradx=A*np.cos(omega*t+phi/360.*2.*np.pi)+B
    
    vg=1/(rhoc*f)*pgradx
    ug=-1./(rhoc*f)*pgrady

    vvec_all[t]=vvec_all[t-1]+(-f*(uvec_all[t-1]-ug)-lda*vvec_all[t-1])*dt
    uvec_all[t]=uvec_all[t-1]+(f*(vvec_all[t]-vg)-pgradx/rhoc-lda*uvec_all[t-1])*dt
    tvec[t]=t




#%% Take daily mean
umean=(uvec_all[0:86400]+uvec_all[86400:172800])/2.
vmean=(vvec_all[0:86400]+vvec_all[86400:172800])/2.

    
    
#%%
plt.figure(num=None, figsize=(10,7),dpi=150, facecolor='w', edgecolor='k')
plt.plot(tvec/3600.,uvec_all, 'b-',linewidth=2)
plt.plot(hourvec[:24],u0mvec[24:], 'r--',linewidth=2)
plt.ylabel(r'U [ms$^{-1}$]',fontsize=15)
plt.xlabel('Time [s]',fontsize=15)
plt.xlim([0,24])
plt.tick_params(axis='both', which='major', labelsize=10)
plt.legend(['approximation','measurements'])

plt.figure(num=None, figsize=(10,7),dpi=150, facecolor='w', edgecolor='k')
plt.plot(tvec[0:86400]/3600.,vmean, 'b-',linewidth=2)
plt.plot(hourvec[:24],v0mvec[24:], 'r--',linewidth=2)
plt.ylabel(r'V [ms$^{-1}$]',fontsize=15)
plt.xlabel('Time [s]',fontsize=15)
plt.xlim([0,24])
plt.tick_params(axis='both', which='major', labelsize=10)
plt.legend(['approximation','measurements'])

