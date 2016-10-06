# ------------------------------------------------------
# Getting amount of CTD and 
# ------------------------------------------------------

which_depth=10 #meters
directory_CTD = 'C:\Users\Mark\Documents\Studie\MAIO_zip\MAIO/CTD_1m/'
CTD_files = glob.glob(directory_CTD+'*')
which_CTD_vec=np.arange(0,63,1)
which_SCAMP_vec=np.arange(0,36,1)
Depth_matrix=[]
Temp_matrix_s=[]
Lat_vec_s=[]
Lon_vec_s=[]
Temp_matrix_c=[]
Lat_vec_c=[]
Lon_vec_c=[]

# ------------------------------------------------------
# Start iteration
# ------------------------------------------------------
for number in range(0,len(which_CTD_vec)+len(which_SCAMP_vec)):
    if number<63:
        which_CTD=which_CTD_vec[number]
        which_SCAMP=1
    else:
        which_SCAMP=which_SCAMP_vec[number-63]
        which_CTD=1

# ------------------------------------------------------
# Defining parameters
# ------------------------------------------------------
    
    Parameter_initial={
        'which_CTD':which_CTD,
        'which_SCAMP':which_SCAMP
        }
    To_compare='temp'

# ------------------------------------------------------
# Get data
# ------------------------------------------------------

    if number<63:
        data=ReadData(Parameter_initial,comparison=To_compare,initialvalue=0)
        data.GetCTDData()
    else:
        data_c=ReadData(Parameter_initial,comparison=To_compare,initialvalue=0)
        data_c.GetCTDData()
        data_s=ReadData(Parameter_initial,comparison=To_compare,initialvalue=0)
        data_s.GetScampData()
        data_comp=ReadData(Parameter_initial,comparison=To_compare,initialvalue=0)
        data_comp.SegmentDataAtDepth(data_s.temp_acc,data_c.temp,data_s.depth,data_c.depth,which_depth)
    
# ------------------------------------------------------
# Save relevant data at every iteration
# ------------------------------------------------------
    
    if number<63:
        for j in range(0,len(data.depth)):
            if data.depth[j]==which_depth:
                Temp_matrix_c.append(data.temp[j])
                Lon_vec_c.append(data.lon)
                Lat_vec_c.append(data.lat)
                print(number)
    else:
        for j in range(0,len(data_comp.depth)):
            if data_comp.depth[j]==which_depth:
                if isnan(data_comp.temp_s[j])==False:
                    Temp_matrix_s.append(data_comp.temp_s[j])
                    Lon_vec_s.append(data_s.lon)
                    Lat_vec_s.append(data_s.lat)
                    print(number)

#%%
# ------------------------------------------------------
# Get Bathymetry
# ------------------------------------------------------

data=ReadData(Parameter_initial,comparison=To_compare,initialvalue=0)
data.GetBathymetryData()
Lat_bath=data.Lat_bath
Lon_bath=data.Lon_bath
Depth=data.Depth

    
#%%
# ------------------------------------------------------
# Plot temperatures of CTD horizontally
# ------------------------------------------------------
only_CTD=0
only_SCAMP=0

if only_CTD==1 and only_SCAMP==0:
    Lon_vec2=Lon_vec_c
    Lat_vec2=Lat_vec_c
    Temp_matrix2=Temp_matrix_c
if only_SCAMP==1 and only_CTD==0:
    Lon_vec2=Lon_vec_s
    Lat_vec2=Lat_vec_s
    Temp_matrix2=Temp_matrix_s
if only_CTD==0 and only_SCAMP==0:
    Lon_vec2=Lon_vec_c+Lon_vec_s
    Lat_vec2=Lat_vec_c+Lat_vec_s
    Temp_matrix2=Temp_matrix_c+Temp_matrix_s    

from scipy.interpolate import griddata
from mpl_toolkits.basemap import Basemap
from matplotlib.mlab import griddata
import matplotlib.colors as colors

plt.figure(figsize=(15,10))
m = Basemap(projection = 'merc',
llcrnrlat=17, urcrnrlat=18.1,
llcrnrlon=-64.5, urcrnrlon=-60.3,
#llcrnrlon=-64, urcrnrlon=-63,
resolution='i', area_thresh=0.001)

xi = np.linspace(np.min(Lon_vec2),np.max(Lon_vec2), 30)
yi = np.linspace(np.min(Lat_vec2),np.max(Lat_vec2),30)
points = np.transpose([Lon_vec2,Lat_vec2])
zi = griddata(Lon_vec2,Lat_vec2, Temp_matrix2, xi, yi, interp='linear')

Matrix=np.zeros(shape=(len(yi),len(yi)))
for i in range(0,len(yi)):
    for j in range(0,len(xi)):
        if np.isnan(zi[i][j])==True:
            Matrix[i][j]==0
        else:
            Matrix[i][j]=zi[i][j]
        
x,y=m(xi,yi)
c=plt.contourf(x,y,Matrix,25,vmin=28.7,vmax=29.8,cmap=plt.cm.jet)
x1,y1=m(Lon_bath,Lat_bath)
b=contours=plt.contour(x1,y1,-Depth,levels=[15,75,250,1000,5000],cmap=plt.cm.Greys,norm=colors.LogNorm(vmin=3,vmax=10000))

x1,y1=m(Lon_bath,Lat_bath)
d=plt.contourf(x1,y1,-Depth,levels=[0,which_depth],colors='white')

lon,lat=m(Lon_vec_s,Lat_vec_s)
m.scatter(lon,lat,s=40,alpha=0.7,c='k',marker=(5, 2))
lon,lat=m(Lon_vec_c,Lat_vec_c)
m.scatter(lon,lat,s=25,alpha=0.7,c='k')
cbar = m.colorbar(c, extend='both', location='bottom',pad="10%")

m.drawcoastlines(linewidth=0.2)
m.drawcountries()
m.drawmapboundary(fill_color='white')
m.fillcontinents(color='chocolate')#'#cc9966')#,lake_color='#99ffff')
par = m.drawparallels(np.arange(15,20,0.5),labels=[1,0,0,0])
mer = m.drawmeridians(np.arange(-65,-59,1),labels=[0,0,0,1])