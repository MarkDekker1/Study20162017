fig= plt.figure(figsize=(10,12))
deepest1=50
deepest2=1500
colorbarused1=plt.cm.rainbow
colorbarused2=plt.cm.coolwarm
colorstationlines='white'
colorbottom='k'
transparency=0.7#0.7#0.0
OrderContour=15
Amountcontours=15
vmina=27.5
vmaxa=30
vminb=4
vmaxb=30
size=125
dev=1
extra=1

# ------------------------------------------------------
# Plot1
# ------------------------------------------------------

plt.subplot(211)


Stations_dist=[]
for i in range(0,len(Stations1)):
    Stations_dist.append(Distance(Lat1[0],Lat1[i],Lon1[0],Lon1[i]))
end=len(Lat1)-1
Horvec=np.linspace(0,max(Stations_dist),1000)

data=ReadData(Parameter_initial,comparison=To_compare,initialvalue=0)
data.GetStraightBathymetry(Lat1[end-dev],Lat1[0],Lon1[end-dev],Lon1[0],1000)
a=data.Depth_vector

xi = np.linspace(np.min(Stations_dist),np.max(Stations_dist), 1000)
yi = np.linspace(2,deepest1,1000)
points = np.transpose([np.array(Stations_dist),Depth_vec])

xvec=[]
yvec=[]
temp1_new=[]
for i in range(0,len(Stations_dist)):
    for j in range(0,len(Depth1[i])):
        xvec.append(Stations_dist[i])
        yvec.append(Depth1[i][j])
        temp1_new.append(Temp1[i][j])

zi = griddata(xvec,yvec, temp1_new, xi, yi, interp='linear')

cs=plt.contourf(xi,-yi,zi,100,cmap=colorbarused1,zorder=5,vmin=vmina,vmax=vmaxa)
plt.contour(xi,-yi,zi,Amountcontours,zorder=OrderContour,colors='k')
plt.scatter(Stations_dist,-np.array(MaximaMatrix(Depth1)),s=size,c='orange',alpha=1,zorder=52,edgecolor='k',linewidth=2,label='Measuring Stations')
for i in range(0,len(Stations_dist)):
    ind=Stations_dist[i]
    plt.plot([ind,ind], [-deepest1,0],'--',color=colorstationlines,linewidth=2,zorder=51)

plt.fill_between(Horvec[::-1], -10000, a, facecolor=colorbottom,zorder=50)#saddlebrown
plt.plot(Horvec[::-1],a,'k',linewidth=3,zorder=51)

f=interpolate.interp1d(Stations_dist,MaximaMatrix(Depth1))
a=f(Horvec)
plt.ylim([-deepest1,-2])
plt.xlim([0,max(Horvec)])
plt.ylabel('Depth (m)',fontsize=15)
plt.tick_params(axis='both', which='major', labelsize=15)
plt.tick_params(axis='x',which='both',bottom='off',top='off',labelbottom='off')
fig.subplots_adjust(right=0.8)
cbar_ax = fig.add_axes([0.85, 0.58, 0.05, 0.3])
a=fig.colorbar(cs3, cax=cbar_ax)
a.ax.tick_params(labelsize=15)
a.set_label(r'Temperature ($^0$C)',size=15)

# ------------------------------------------------------
# Plot2
# ------------------------------------------------------

plt.subplot(212)
Stations_dist=[]
for i in range(0,len(Stations1)):
    Stations_dist.append(Distance(Lat1[0],Lat1[i],Lon1[0],Lon1[i]))
end=len(Lat1)-1
Horvec=np.linspace(0,max(Stations_dist),1000)

data=ReadData(Parameter_initial,comparison=To_compare,initialvalue=0)
data.GetStraightBathymetry(Lat1[end-dev],Lat1[0],Lon1[end-dev],Lon1[0],1000)
a=data.Depth_vector

xi = np.linspace(np.min(Stations_dist),np.max(Stations_dist), 1000)
yi = np.linspace(2,deepest2,1000)
points = np.transpose([np.array(Stations_dist),Depth_vec])

xvec=[]
yvec=[]
temp1_new=[]
for i in range(0,len(Stations_dist)):
    for j in range(0,len(Depth1[i])):
        xvec.append(Stations_dist[i])
        yvec.append(Depth1[i][j])
        temp1_new.append(Temp1[i][j])

zi = griddata(xvec,yvec, temp1_new, xi, yi, interp='linear')

cs=plt.contourf(xi,-yi,zi,100,cmap=colorbarused2,zorder=5,vmin=vminb,vmax=vmaxb)
plt.contour(xi,-yi,zi,Amountcontours,zorder=OrderContour,colors='k')
plt.scatter(Stations_dist,-np.array(MaximaMatrix(Depth1)),s=size,c='orange',alpha=1,zorder=52,edgecolor='k',linewidth=2,label='Measuring Stations')
for i in range(0,len(Stations_dist)):
    ind=Stations_dist[i]
    plt.plot([ind,ind], [-deepest2,0],'--',color=colorstationlines,linewidth=2,zorder=51)

if extra==0:
    for j in range(0,len(unique(Stations_dist))):
        #plt.scatter(Stations_dist,zeros(len(Stations_dist)),s=200,c='orange',alpha=1,zorder=52,edgecolor='k',linewidth=2)
        plt.text(unique(Stations_dist)[j]-0.025*Stations_dist[len(Stations_dist)-1],deepest2/16.,Stations1_s[j],fontsize=21,zorder=53,fontweight='bold')
if extra==1:
    for j in range(0,len(unique(Stations_dist))):
        
        if j!=1:
            plt.text(unique(Stations_dist)[j]-0.025*Stations_dist[len(Stations_dist)-1],deepest2/16.,Stations1_s[j],fontsize=21,zorder=53,fontweight='bold')
        if j==1:
            plt.text(unique(Stations_dist)[j]-0.065*Stations_dist[len(Stations_dist)-1],deepest2/16.,Stations1_s[j],fontsize=21,zorder=54,fontweight='bold')

plt.fill_between(Horvec[::-1], -10000, a, facecolor=colorbottom,zorder=50)#saddlebrown
plt.plot(Horvec[::-1],a,'k',linewidth=3,zorder=51)
f=interpolate.interp1d(Stations_dist,MaximaMatrix(Depth1))
a=f(Horvec)
plt.ylim([-deepest2,-2])
plt.xlim([0,max(Horvec)])
plt.xlabel('Horizontal distance (km)',fontsize=15)
plt.ylabel('Depth (m)',fontsize=15)
plt.tick_params(axis='both', which='major', labelsize=15)
fig.subplots_adjust(right=0.8)
cbar_ax = fig.add_axes([0.85, 0.15, 0.05, 0.3])
a=fig.colorbar(cs, cax=cbar_ax)
a.ax.tick_params(labelsize=15)
a.set_label(r'Temperature ($^0$C)',size=15)
