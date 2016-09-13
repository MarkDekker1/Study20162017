#%% Check:
ACF2=stat.acf(FIT)
PACF2=stat.pacf(FIT)
Timelags=np.linspace(0,40,41)
    
plt.figure(num=None, figsize=(10,3),dpi=150, facecolor='w', edgecolor='k')
plt.plot(FIT, 'k-',linewidth=3)
plt.ylabel('Data',fontsize=20)
plt.xlabel('Time',fontsize=20)
plt.tick_params(axis='both', which='major', labelsize=20)

plt.figure(num=None, figsize=(5,3),dpi=150, facecolor='w', edgecolor='k')
plt.scatter(Timelags,ACF2, alpha=0.5,s=150)
plt.plot(Timelags,ACF2)
plt.ylabel('Data',fontsize=20)
plt.xlim([-0.5,20.5])
plt.xlabel('Time',fontsize=20)
plt.tick_params(axis='both', which='major', labelsize=20)

plt.figure(num=None, figsize=(5,3),dpi=150, facecolor='w', edgecolor='k')
plt.scatter(Timelags,PACF2, alpha=0.5,s=150)
plt.plot(Timelags,PACF2)
plt.ylabel('Data',fontsize=20)
plt.xlabel('Time',fontsize=20)
plt.xlim([-0.5,20.5])
plt.tick_params(axis='both', which='major', labelsize=20)



#%%Plot data

ACF=stat.acf(ARdata)
PACF=stat.pacf(ARdata)
length2=len(ACF)

Timelags=np.linspace(0,40,41)
plt.figure(num=None, figsize=(10,3),dpi=150, facecolor='w', edgecolor='k')
plt.plot(ARdata, 'k-',linewidth=1)
plt.ylabel('Data',fontsize=20)
plt.xlabel('Time',fontsize=20)
plt.tick_params(axis='both', which='major', labelsize=20)


#Plot autocorrelation function
plt.figure(num=None, figsize=(5,3),dpi=150, facecolor='w', edgecolor='k')
plt.scatter(Timelags,ACF, alpha=0.5,s=150)
plt.plot(Timelags,ACF)
plt.ylabel('ACF',fontsize=20)
plt.xlabel('Time lag',fontsize=20)
plt.xlim([-0.5,20.5])
plt.tick_params(axis='both', which='major', labelsize=20)

#Plot partial autocorrelation function
plt.figure(num=None, figsize=(5,3),dpi=150, facecolor='w', edgecolor='k')
plt.scatter(Timelags,PACF, alpha=0.5,s=150)
plt.plot(Timelags,PACF)
plt.ylabel('PACF',fontsize=20)
plt.xlabel('Time lag',fontsize=20)
plt.xlim([-0.5,20.5])
plt.tick_params(axis='both', which='major', labelsize=20)