
from scipy.spatial import cKDTree as KDTree
from scipy import interpolate

x=Lon_vec
y=Lat_vec
z=dissipation

xx,yy=np.meshgrid(x,y)
f=interpolate.interp1d(x,y,z,kind='linear')
znew=f(x,y)
#%%

import matplotlib.mlab as mlab

x=Lon_vec
y=Lat_vec
z=dissipation

xmin=np.min(Lon_vec)
xmax=np.max(Lon_vec)
ymin=np.min(Lat_vec)
ymax=np.max(Lat_vec)
nx=10
ny=10

# Generate a regular grid to interpolate the data.
xi = np.linspace(xmin, xmax, nx)
yi = np.linspace(ymin, ymax, ny)
xi, yi = np.meshgrid(xi, yi)

# Interpolate using delaunay triangularization 
zi = mlab.griddata(x,y,z,xi,yi)
#%%
def normalize_x(data):
    data = data.astype(np.float)
    return (data - xmin) / (xmax - xmin)

def normalize_y(data):
    data = data.astype(np.float)
    return (data - ymin) / (ymax - ymin)

x_new, xi_new = normalize_x(x), normalize_x(xi)
y_new, yi_new = normalize_y(y), normalize_y(yi)

# Interpolate using delaunay triangularization 
zi = mlab.griddata(x_new, y_new, z, xi_new, yi_new)


#%%
grid_x, grid_y = meshgrid(Lon_vec,Lat_vec)
points = np.transpose([Lon_vec,Lat_vec])
values = dissipation
from scipy.interpolate import griddata
#grid_z0 = griddata(points, values, (grid_x, grid_y), method='nearest')
grid_z1 = griddata(points, values, (grid_x, grid_y), method='linear')
#grid_z2 = griddata(points, values, (grid_x, grid_y), method='cubic')
#%%
import matplotlib.pyplot as plt
plt.subplot(221)
plt.imshow(func(grid_x, grid_y).T, extent=(0,1,0,1), origin='lower')
plt.plot(points[:,0], points[:,1], 'k.', ms=1)
plt.title('Original')
plt.subplot(222)
plt.imshow(grid_z0.T, extent=(0,1,0,1), origin='lower')
plt.title('Nearest')
plt.subplot(223)
plt.imshow(grid_z1.T, extent=(0,1,0,1), origin='lower')
plt.title('Linear')
plt.subplot(224)
plt.imshow(grid_z2.T, extent=(0,1,0,1), origin='lower')
plt.title('Cubic')
plt.gcf().set_size_inches(6, 6)
plt.show()
#%%
from scipy import interpolate
>>> x = np.arange(-5.01, 5.01, 0.25)
>>> y = np.arange(-5.01, 5.01, 0.25)
>>> xx, yy = np.meshgrid(x, y)
>>> z = np.sin(xx**2+yy**2)
>>> f = interpolate.interp2d(x, y, z, kind='cubic')

import matplotlib.pyplot as plt
>>> xnew = np.arange(-5.01, 5.01, 1e-2)
>>> ynew = np.arange(-5.01, 5.01, 1e-2)
>>> znew = f(xnew, ynew)
>>> plt.plot(x, z[0, :], 'ro-', xnew, znew[0, :], 'b-')
>>> plt.show()
#%%
x = np.asarray([0, 1, 2, 3, 0.5, 1.5, 2.5, 1, 2, 1.5])
y = np.asarray([0, 0, 0, 0, 1.0, 1.0, 1.0, 2, 2, 3.0])
triangles = [[0, 1, 4], [1, 2, 5], [2, 3, 6], [1, 5, 4], [2, 6, 5], [4, 5, 7],
             [5, 6, 8], [5, 8, 7], [7, 8, 9]]
triang = mtri.Triangulation(x, y, triangles)