# ------------------------------------------------------
# Process data
# ------------------------------------------------------

which_SCAMP=22
which_CTD=9

down_cast = argmax(depth_s)
surface = argmin(fabs(np.asarray(depth_s[down_cast:]) - 2.0)) + down_cast + 1
lon_point = lon_all_s[which_SCAMP]
lat_point = lat_all_s[which_SCAMP]

# ------------------------------------------------------
# Plot Temperatures of SCAMP and CTD at chosen stations
# ------------------------------------------------------

plt.figure(num=None, figsize=(8,4),dpi=150, facecolor='w', edgecolor='k')
plt.plot(temp_acc_s[:down_cast],depth_s[:down_cast], 'r-',linewidth=2)
plt.plot(temp_acc_s[down_cast:surface],depth_s[down_cast:surface], 'k-',linewidth=2)
plt.plot(temp_c,depth_c, 'b-',linewidth=2)
plt.ylabel('Depth [m]',fontsize=15)
plt.xlabel('Temperature [K]',fontsize=15)
plt.tick_params(axis='both', which='major', labelsize=15)
#plt.ylim([max(list(depth_c)+list(depth_s)) + 5, min(list(depth_c)+list(depth_s)) - 0.5])
plt.ylim([max(list(depth_s)) + 5, min(list(depth_s)) - 0.5])
plt.xlim([min(list(temp_acc_s[:down_cast])) - 0.5,max(list(temp_acc_s[:down_cast])) + 0.5])
plt.legend(['SCAMP, down','SCAMP, up','CTD'],loc='best')

# ------------------------------------------------------
# Create map showing the point
# ------------------------------------------------------

from mpl_toolkits.basemap import Basemap

plt.figure(figsize=(5,5))
m = Basemap(projection = 'merc',
llcrnrlat=lat_point-0.5, urcrnrlat=lat_point+0.5,
llcrnrlon=lon_point-0.8, urcrnrlon=lon_point+0.8,
resolution='i', area_thresh=0.001)

m.drawcoastlines(linewidth=0.2)
m.drawcountries()
m.drawmapboundary(fill_color='#99ffff')
m.fillcontinents(color='#cc9966',lake_color='#99ffff')
par = m.drawparallels(np.arange(15,20,0.2),labels=[1,0,0,0])
mer = m.drawmeridians(np.arange(-65,-59,0.5),labels=[0,0,0,1])

x, y = m(lon_point,lat_point)
m.scatter(x, y, s = 16, color ='k')
if which_SCAMP != 11:
    x, y = m(lon_point, lat_point)
else:
    x, y = m(lon_point, lat_point)
plt.text(x,y-10000,which_CTD+1,fontsize=15,fontweight='bold', ha='center',va='center',color='r')
plt.text(x,y+10000,which_SCAMP+1,fontsize=15,fontweight='bold', ha='center',va='center',color='k')

# ------------------------------------------------------
# Segment SCAMP (1 m) (assuming depth profile CTD is equidistant for Dz=1 m)
# ------------------------------------------------------

segmented_temp=[]
segmented_depth=[]
segmented_error=[]
for i in range(np.int(min(depth_c)),np.int(max(depth_s))):
    depth_max=np.float(i)+0.5
    depth_min=np.float(i-1)-0.5
    segment_data=[]    
    for k in range(0,len(depth_s)):
        if depth_s[k]<depth_max and depth_s[k]>=depth_min:
            segment_data.append(temp_acc_s[k])
    segmented_temp.append(np.mean(segment_data))
    segmented_depth.append(i)
    segmented_error.append(np.mean(segment_data)-temp_c[i-np.int(depth_c[0])])

# ------------------------------------------------------
# Plot error between segmented SCAMP and CTD
# ------------------------------------------------------

plt.figure(num=None, figsize=(8,4),dpi=150, facecolor='w', edgecolor='k')
plt.plot(segmented_error,segmented_depth, 'r-',linewidth=2)
plt.ylabel('Depth [m]',fontsize=15)
plt.xlabel('Temperature [K]',fontsize=15)
plt.ylim([max(list(depth_s)) + 5, min(list(depth_s)) - 0.5])
plt.tick_params(axis='both', which='major', labelsize=15)