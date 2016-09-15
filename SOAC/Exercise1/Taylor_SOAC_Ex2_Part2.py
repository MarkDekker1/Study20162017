#Taylor diagram
u_meas=u0mvec[24:]
u_mod=umean[0:86400:3600]
time_end=hourvec[:24]

#Correlation coefficient
R=np.corrcoef(u_meas,u_mod)

#Standard deviations
sigma_meas=np.sqrt(np.var(u_meas))
sigma_mod=np.sqrt(np.var(u_mod))

#Error
