# ------------------------------------------------------
# Preambule
# ------------------------------------------------------

from mpl_toolkits.basemap import Basemap
lon_all_s=Lon_vec_s
lon_all_c=Lon_vec_c
lat_all_s=Lat_vec_s
lat_all_c=Lat_vec_c


# ------------------------------------------------------
# Start Basemap
# ------------------------------------------------------

plt.figure(figsize=(30,25))
m = Basemap(projection = 'merc',
llcrnrlat=17, urcrnrlat=18,
llcrnrlon=-64.5, urcrnrlon=-60.3,
resolution='i', area_thresh=0.001)

m.drawcoastlines(linewidth=0.2)
m.drawcountries()
m.drawmapboundary(fill_color='#99ffff')
m.fillcontinents(color='#cc9966',lake_color='#99ffff')
par = m.drawparallels(np.arange(15,20,1),labels=[1,0,0,0])
mer = m.drawmeridians(np.arange(-65,-59,1),labels=[0,0,0,1])
stations_s	= which_SCAMP_vec#np.arange(1, len(lon_all_s) + 1)
stations_c	= which_CTD_vec#np.arange(1, len(lon_all_c) + 1)

# ------------------------------------------------------
# Plot SCAMP stations
# ------------------------------------------------------

x, y = m(lon_all_s, lat_all_s)
m.scatter(x, y, s = 16, color ='k')
for stations_i in range(len(stations_s)):
	if stations_i != 11:
		x, y = m(lon_all_s[stations_i], lat_all_s[stations_i]+0.05)
	else:
		x, y = m(lon_all_s[stations_i]+0.05, lat_all_s[stations_i]+0.01)
	plt.text(x,y,stations_s[stations_i],fontsize=15,fontweight='bold', ha='center',va='center',color='k')

# ------------------------------------------------------
# Plot CTD stations
# ------------------------------------------------------
 
x, y = m(lon_all_c, lat_all_c)
m.scatter(x, y, s = 16, color ='r')
for stations_i in range(len(stations_c)):
    x, y = m(lon_all_c[stations_i], lat_all_c[stations_i])
    plt.text(x,y-10000.,stations_c[stations_i],fontsize=15,fontweight='bold', ha='center',va='top',color='r')
show()