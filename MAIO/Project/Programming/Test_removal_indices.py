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
            
month_list = ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC']
file = open(directory_SCAMP+year+month+day+'/'+day+month_list[int(month) - 1]+year+' '+time_ms+'.pro', 'r')
lines_raw = file.readlines()
file.close()

file_ind = open('Remove_indices_v1.txt','r')        
lines_ind=file_ind.readlines()
file_ind.close()
line_spec=lines_ind[which_SCAMP+1].split()

lines_noupcast=lines_raw[:np.int(line_spec[8])] # remove upcast
matrix_lines=[]
for i in [2,4,6]:
    if not isnan(np.float(line_spec[i])):
        matrix_lines.append(lines_noupcast[:np.int(line_spec[i])]+lines_noupcast[np.int(line_spec[i+1]):])

lines=lines_noupcast
if len(matrix_lines)>0:
    lines_touse=matrix_lines[0]
    for i in range(1,len(matrix_lines)):
        lines_touse=lines_touse+matrix_lines[i]
    lines=lines_touse

print(time_ms)
print(line_spec[1])

#%%
data_s=ReadData(Parameter_initial,comparison=To_compare,initialvalue=0)
data_s.GetScampData()