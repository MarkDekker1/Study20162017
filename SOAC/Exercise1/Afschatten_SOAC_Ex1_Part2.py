
#%%Afschatten A, phi
tvec=[]
for t in range(0,86400):
    tvec.append(t*dt)


phivec=np.linspace(-150,0,100)
Avec=np.linspace(0.0001,0.0013,100)
Epmatrix=[]
for TryPhi in phivec:
    Epvec=[]
    for TryA in Avec:
        pgradx=[]
        for t in np.arange(86400,172800,3600):
            pgradx.append(TryA*np.cos(omega*t+TryPhi/360.*2.*np.pi))
        
        Epvec.append(np.sum((pgradx-dpdxmvec[24:])**2))
    Epmatrix.append(Epvec)

#%% Plot voor afschatten
plt.figure(num=None, figsize=(10, 8), dpi=100, facecolor='w', edgecolor='k')
cs=plt.contourf(Avec,phivec,Epmatrix,200,cmap=cm.coolwarm)
plt.contour(Avec,phivec,Epmatrix,25,linewidth=3.0,colors='k')
cbar = plt.colorbar(cs)
plt.ylabel('Phi [deg]',fontsize=15)
plt.xlabel(r'A [hPa m$^{-1}$]',fontsize=15)
plt.tick_params(axis='both', which='major', labelsize=10)


#find minima
Aindex=np.where(Epmatrix==np.min(Epmatrix))[1]
phiindex=np.where(Epmatrix==np.min(Epmatrix))[0]


A=Avec[Aindex]
phi=phivec[phiindex]

pgradx=[]
for t in range(0,86400):
    pgradx.append(A*np.cos(omega*t+phi/360.*2.*np.pi))

plt.figure(num=None, figsize=(7,3),dpi=150, facecolor='w', edgecolor='k')
plt.plot(tvec,pgradx, 'b-',linewidth=2)
plt.plot(timevec[:24],dpdxmvec[24:], 'ro',linewidth=2)
plt.ylabel(r'$\frac{\partial p}{\partial x}$ [hPa m$^{-1}$]',fontsize=15)
plt.xlabel('Time [s]',fontsize=15)
plt.tick_params(axis='both', which='major', labelsize=10)


#%%Afschatten M, theta
tvec=[]
for t in range(0,172800):
    tvec.append(t*dt)


thetavec=np.linspace(-300,-50,100)
Mvec=np.linspace(0.00005,0.003,100)
Epmatrix=[]
for Trytheta in thetavec:
    Epvec=[]
    for TryM in Mvec:
        pgrady=[]
        for t in np.arange(0,172800,3600):
            pgrady.append(TryM*np.cos(omega*t+Trytheta/360.*2.*np.pi))
        
        Epvec.append(np.sum((pgrady-dpdyvec)**2))
    Epmatrix.append(Epvec)

#%% Plot voor afschatten
plt.figure(num=None, figsize=(10, 8), dpi=100, facecolor='w', edgecolor='k')
cs=plt.contourf(Mvec,thetavec,Epmatrix,200,cmap=cm.coolwarm)
plt.contour(Mvec,thetavec,Epmatrix,50,linewidth=3.0,colors='k')
cbar = plt.colorbar(cs)
plt.ylabel('Theta [deg]',fontsize=15)
plt.xlabel(r'M [hPa m$^{-1}$]',fontsize=15)
plt.tick_params(axis='both', which='major', labelsize=10)


#find minima
Mindex=np.where(Epmatrix==np.min(Epmatrix))[1]
thetaindex=np.where(Epmatrix==np.min(Epmatrix))[0]


M=Mvec[Mindex]
theta=thetavec[thetaindex]

pgrady=[]
for t in range(0,172800):
    pgrady.append(M*np.cos(omega*t+theta/360.*2.*np.pi))

plt.figure(num=None, figsize=(7,3),dpi=150, facecolor='w', edgecolor='k')
plt.plot(tvec,pgrady, 'b-',linewidth=2)
plt.plot(timevec,dpdyvec, 'ro',linewidth=2)
plt.ylabel(r'$\frac{\partial p}{\partial x}$ [hPa m$^{-1}$]',fontsize=15)
plt.xlabel('Time [s]',fontsize=15)
plt.tick_params(axis='both', which='major', labelsize=10)
