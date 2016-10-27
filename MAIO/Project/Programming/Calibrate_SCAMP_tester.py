# ------------------------------------------------------
# Redefining for clarity
# ------------------------------------------------------

plt.style.use('ggplot')
temp_c=data_c.temp
temp_s=data_s.temp_acc
depth_c=data_c.depth
depth_s=data_s.depth
# ------------------------------------------------------
# Find optimal calibration constant
# ------------------------------------------------------

Parameter_initial={
    'which_CTD':which_CTD,
    'which_SCAMP':which_SCAMP
    }
To_compare='temp'
data_comp=ReadData(Parameter_initial,comparison=To_compare,initialvalue=0)
data_comp.SegmentData(temp_s,temp_c,depth_s,depth_c)
seg_temp_c=data_comp.temp_c
seg_temp_s=data_comp.temp_s
seg_depth=np.array(data_comp.depth)
seg_error=data_comp.error

S_matrix=[seg_temp_s]
E_matrix=[seg_error]
C_matrix=[seg_temp_c]

vectortje=where(np.array(data_s.depth)>2)[0]
vectortje2=[]
for i in range(0,len(vectortje)):
    vectortje2.append(np.int(vectortje[i]))

plt.figure(num=None, figsize=(8,4),dpi=150, facecolor='w', edgecolor='k')
plt.plot(seg_temp_c,seg_depth,'k-',label='CTD', linewidth=4)
plt.plot(data_s.temp_acc[0:len(data_s.temp_acc)-3],data_s.depth[0:len(data_s.temp_acc)-3], 'g-',label='SCAMP',linewidth=0.5)
plt.plot(seg_temp_s,seg_depth, 'r-',label='SCAMP seg',linewidth=4)

# ------------------------------------------------------
# Remove error linear with depth (error variance threshold 0.02)
# ------------------------------------------------------

threshold=50000
mtake=4
length=len(seg_temp_s)
if np.var(E_matrix[0])>threshold:
    coefficient=(np.mean(E_matrix[0][0:mtake])-np.mean(E_matrix[0][(length-mtake):(length-1)]))/(seg_depth[length-1]-seg_depth[0])
    coefficient=coefficient
    vec=coefficient*(seg_depth-seg_depth[0])
    S_matrix.append(S_matrix[0]+vec)#-E_matrix[0][0])
    E_matrix.append(S_matrix[1]-seg_temp_c)
    plt.plot(S_matrix[1],seg_depth,'b-',linewidth=2)
else:
    S_matrix.append(S_matrix[0])
    E_matrix.append(E_matrix[0])
    
# ------------------------------------------------------
# Remove lag
# ------------------------------------------------------

D_matrix=[seg_depth]
E_vec=[]
lag_max=np.max([np.min([len(seg_depth)/4,5]),1])
lag_min=-np.max([np.min([len(seg_depth)/4,5]),1])
lag_vec=np.arange(lag_min,lag_max+1,1)
C_new=[]
D_new=[]
E_new=[]
S_new=[]
for i in range(0,len(lag_vec)):
    lag=lag_vec[i]
    D_new.append(seg_depth+lag)
    if lag>0:
        S_new.append(np.array(S_matrix[1][0:(length-lag)]))
        C_new.append(np.array(C_matrix[0][lag:length]))
        D_new[i]=D_new[i][0:np.int(length-lag)]
    if lag<0:
        lag=np.abs(lag)
        S_new.append(np.array(S_matrix[1][lag:length]))
        C_new.append(np.array(C_matrix[0][0:(length-lag)]))
        D_new[i]=D_new[i][lag:length]
    if lag==0:
        S_new.append(np.array(S_matrix[1]))
        C_new.append(np.array(C_matrix[0]))
    E_new.append(np.array(S_new[i]-C_new[i]))
    E_vec.append(np.nanvar(E_new[i])/len(E_new))
    
if E_vec[where(lag_vec==0)[0][0]]>np.nanmin(E_vec)*3:
    finder=where(E_vec==np.nanmin(E_vec))
else:
    finder=[where(lag_vec==0)[0]]

finder=finder[0][0]
Best_lag=lag_vec[finder]
Best_D=D_new[finder]
Best_C=C_new[finder]
Best_E=E_new[finder]
Best_S=S_new[finder]
#plt.plot(Best_S,Best_D,'g--',label='Lag removed',linewidth=2)

# ------------------------------------------------------
# Remove constant bias
# ------------------------------------------------------

Best_S = Best_S-np.mean(Best_E)
Best_E2 = Best_S-Best_C
 
plt.plot(Best_S,Best_D,'m-',label='Approximation',linewidth=2)    
plt.ylabel('Depth [m]',fontsize=15)
plt.xlabel(r'Temperature [$^0 C$]',fontsize=15)
plt.tick_params(axis='both', which='major', labelsize=15)
plt.ylim([np.max(seg_depth)+5,0])

plt.legend(loc='best',prop={'size':13})

E0=mean(sqrt(np.array(E_matrix[0])**2))
E_lin=mean(sqrt(np.array(E_matrix[1])**2))
E_linlag=mean(sqrt(Best_E**2))
E_linlagbias=mean(sqrt(Best_E2**2))