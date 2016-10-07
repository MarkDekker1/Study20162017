# ------------------------------------------------------
# Preambule
# ------------------------------------------------------

from pylab import *
import numpy
import datetime
import time
import glob, os
import math
import netCDF4 as netcdf
import matplotlib.colors as colors
import matplotlib.cm as cmx
import matplotlib.pyplot as plt
#from mpl_toolkits.basemap import Basemap
matplotlib.style.use('ggplot')

# ------------------------------------------------------
# Class
# ------------------------------------------------------

class Mercator(object):

# ------------------------------------------------------
# Initialization
# ------------------------------------------------------    
    
    def __init__(self,parameters,initialvalue=None):
        self.P = dict.fromkeys(['which_CTD'])
        self.P.update(parameters)
        which_CTD = self.P['which_CTD']-1
        
# ------------------------------------------------------
# Locate nearest point of Mercator and gain data from there
# ------------------------------------------------------   
        
    def DataStation(self):
        directory_CTD = 'C:\Users\Mark\Documents\Studie\MAIO_zip\MAIO/CTD_1m/'
        CTD_files = glob.glob(directory_CTD+'*')
        self.temp_c, theta, cond, pres, self.depth_c, salt, dens, self.time, fluor, self.date, lon_c, lat_c, hour_c, minute_c, second,day_c= ReadinCTDData(CTD_files[which_CTD])
        
        index_lon=np.int(12*(lon_c+80))
        index_lat=np.int(12*(lat_c))
        
        DataSet = netcdf.Dataset('C:\Users\Mark\Documents\Studie\Data\MAIO_Project/Mercator_2h_august_18_september_7.nc', mode='r')
        date	= DataSet.variables['time_counter'][:] 	#Hours passed since 1-1-1950, 00:00:00
        
        if day_c[0]>=18:
            day_number=day_c[0]-18
        else:
            day_number=day_c[0]+13
        
        index_date=np.int(day_number+np.mod(hour_c[0],24)/2+minute_c[0]/120.)
        
        self.lon		= DataSet.variables['longitude'][index_lon]
        self.lat 	= DataSet.variables['latitude'][index_lat]
        self.u_m	= DataSet.variables['u'][:,index_lat,index_lon]
        self.v_m	= DataSet.variables['v'][:,index_lat,index_lon]
        self.temp_m0= DataSet.variables['temperature'][index_date][index_lat][index_lon]
        self.temp_m= DataSet.variables['temperature'][:,index_lat,index_lon]
        self.SSH	= DataSet.variables['ssh'][:,index_lat,index_lon]
        self.hour = date-date[0]
        self.index = index_date
        
        DataSet.close()