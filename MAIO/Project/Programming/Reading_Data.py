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
from mpl_toolkits.basemap import Basemap

# ------------------------------------------------------
# Choosing stations
# ------------------------------------------------------

which_CTD = 10
which_SCAMP = 23

which_CTD = which_CTD-1
which_SCAMP = which_SCAMP-1

# ------------------------------------------------------
# Pathways
# ------------------------------------------------------

directory_CTD = 'C:\Users\Mark\Documents\Studie\MAIO_zip\MAIO/CTD_1m/'
directory_SCAMP  = 'C:\Users\Mark\Documents\Studie\MAIO_zip\MAIO/Measurements/'
directory_location_scamp 		= 'C:\Users\Mark\Documents\Studie\MAIO_zip\MAIO'
file = open(directory_location_scamp+'\Locations\SCAMP_details.txt', 'r')
lines = file.readlines()
file.close()

for line_i in [which_SCAMP]:
    line = lines[line_i].split()
    day=(line[0][0:2])
    month=(line[0][2:5])
    year=line[0][5:]
    time_ms=(line[1])
if month=='AUG':
    month='08'
else:
    month='09'
    
# ------------------------------------------------------
# Reading SCAMP data (recognized by _s)
# ------------------------------------------------------

month_list = ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC']
file = open(directory_SCAMP+year+month+day+'/'+day+month_list[int(month) - 1]+year+' '+time_ms+'.pro', 'r')
lines = file.readlines()
file.close()

time_s     = [] #Time (sec)
depth_s    = [] #Depth (meter)
velo_s 	= [] #Falling velocity (m/s)
temp_0f_s 	= [] #Temperature (sensor 0, Celsius)
temp_1f_s 	= [] #Temperature (sensor 1, Celsius)
temp_acc_s	= [] #Accurate temperature (Celsius)
cond_f_s   	= [] #Fast conductivity sensor (mS/cm) (will be used to determine salinity)
cond_acc_s	     = [] #Accurate conductivity sensor (mS/cm) (will be used to determine salinity)
tempgrad_0f_s   = [] #Gradient fast temperature sensor 0 (Celsius)
tempgrad_1f_s  = [] #Gradient fast temperature sensor 1 (Celsius)
fluor_s    = [] #Fluorescence (Volt)
sigmaT_s   = [] #Sigma_T, also know as the density - 1000 (kg/m^3)
sigmaT_sort_s= [] #Density stable sorted sigma_T
BVfreq_s   = [] #Brunt-Vaisala frequency (1/sec)
thorpe_s   = [] #Thorpe displacement (meter)
KJ_s       = []
salt_s      = [] #Salinity (PSU = g / kg)


for line_i in range(len(lines)):
	line = lines[line_i].split()	
	time_s.append(float(line[0]))
	depth_s.append(float(line[1]))
	velo_s.append(float(line[2]))
	temp_0f_s.append(float(line[3]))
	temp_1f_s.append(float(line[4]))
	temp_acc_s.append(float(line[5]))
	cond_f_s.append(float(line[6]))
	cond_acc_s.append(float(line[7]))
	tempgrad_0f_s.append(float(line[8]))
	tempgrad_1f_s.append(float(line[9]))
	#Channel 10 is skipped since it contains only Nan's
	fluor_s.append(float(line[11]))
	sigmaT_s.append(float(line[12]))
	sigmaT_sort_s.append(float(line[13]))
	BVfreq_s.append(float(line[14]))
	thorpe_s.append(float(line[15]))
	KJ_s.append(float(line[16]))
	salt_s.append(float(line[17]))
 
down_cast = argmax(depth_s)
surface = argmin(fabs(np.asarray(depth_s[down_cast:]) - 2.0)) + down_cast + 1


directory_location_scamp 		= 'C:\Users\Mark\Documents\Studie\MAIO_zip\MAIO'

file = open(directory_location_scamp+'\Locations\SCAMP_details.txt', 'r')
lines = file.readlines()
file.close()

lat_s 	= np.zeros(len(lines))
lon_s 	= np.zeros(len(lines))
day_s       = np.zeros(len(lines))

for line_i in range(len(lines)):
    line = lines[line_i].split()
    day_s=(line[0][0:2])
    time_ms_s=(line[1])
    
    if day_s==day and time_ms_s==time_ms:
        lat_s=np.float(line[3])
        lon_s=np.float(line[4])

# ------------------------------------------------------
# Reading CTD data (recognized by _c)
# ------------------------------------------------------

CTD_files = glob.glob(directory_CTD+'*')

def ReadinCTDData(filename, directory =''):
	"""Reads in the data of the CTD file, returns array's of temperature, salt etc.
	Input of directory name is optional, not necessary"""

	file = open(directory+filename, 'r')
	lines = file.readlines()
	file.close()
	
	temp_c		= [] #Temperature (Celsius)
	theta_c		= [] #Potential temperature (Celsius)
	cond_c      	= [] #Conductivity (mS/cm)
	pres_c		= [] #Pressure (db)
	depth_c		= [] #Depth (m)
	salt_c  		= [] #Salinity (PSU = g / kg)
	dens_c		= [] #Density - 1000.0 (kg/m^3)
	time_c		= [] #time (sec)
	fluor_c      	= [] #Fluorescence (ug/L)

	for line_i in range(len(lines)):

		if lines[line_i].split()[1:4] == ['NMEA', 'UTC', '(Time)']:
			#Time of measurement
			month, day, year, time = lines[line_i].split()[5:]
			hour, minute, seconds  = time[0:2], time[3:5], time[6:8]

			if month == 'Aug': #Only Augustus or September
				month = 8
			else:
				month = 9
				
			date  = datetime.datetime(year=int(year), month=month, day=int(day)).toordinal() #Date in toordinal form
			date += ((((float(seconds) / 60.0) + float(minute))/60.0) + float(hour))/24.0 #Convert time to days
		
		if lines[line_i].split()[1:3] == ['NMEA', 'Latitude']:
			lat = float(lines[line_i].split()[4]) + float(lines[line_i].split()[5])/60.0
			#The first one is degree, second one minutes (minutes / 60.0 = degrees)
						
		if lines[line_i].split()[1:3] == ['NMEA', 'Longitude']:
			lon = -(float(lines[line_i].split()[4]) + float(lines[line_i].split()[5])/60.0)
			#The first one is degree, second one minutes (minutes / 60.0 = degrees)
			#Including minus sign, so 60W = -60.0
		
		if lines[line_i].split() != ['*END*']:
			continue
			
		else:
			for line_i in range(line_i+1, len(lines)):
				line = lines[line_i].split()
				temp_c.append(float(line[0]))
				theta_c.append(float(line[1]))
				cond_c.append(float(line[2]))
				pres_c.append(float(line[3]))
				depth_c.append(float(line[4]))
				salt_c.append(float(line[5]))
				dens_c.append(float(line[6]))
				time_c.append(float(line[7]))
				fluor_c.append(float(line[8]))
			
			return np.asarray(temp_c), np.asarray(theta_c), np.asarray(cond_c), np.asarray(pres_c), np.asarray(depth_c), np.asarray(salt_c), np.asarray(dens_c), np.asarray(time_c), np.asarray(fluor_c), date, lon, lat

temp_c, theta_c, cond_c, pres_c, depth_c, salt_c, dens_c, time_c, fluor_c, date_c, lon_c, lat_c= ReadinCTDData(CTD_files[which_CTD])

# ------------------------------------------------------
# Retrieving all locations CTD and SCAMP
# ------------------------------------------------------

lon_all_c=np.zeros(len(CTD_files))
lat_all_c=np.zeros(len(CTD_files))
date_all_c=np.zeros(len(CTD_files))
for i in range(0,len(CTD_files)):
    temp_0, theta_0, cond_0, pres_0, depth_0, salt_0, dens_0, time_0, fluor_0, date_all_c[i], lon_all_c[i], lat_all_c[i]= ReadinCTDData(CTD_files[i])


directory_location_scamp 		= 'C:\Users\Mark\Documents\Studie\MAIO_zip\MAIO'

file = open(directory_location_scamp+'\Locations\SCAMP_details.txt', 'r')
lines = file.readlines()
file.close()

lat_all_s 	= np.zeros(len(lines))
lon_all_s 	= np.zeros(len(lines))
day_all_s       = np.zeros(len(lines))

for line_i in range(len(lines)):
    line = lines[line_i].split()
    day_all_s=(line[0][0:2])
    time_ms_s=(line[1])
    lat_all_s[line_i]=np.float(line[3])
    lon_all_s[line_i]=np.float(line[4])