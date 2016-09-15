#Preambule
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.tsa.stattools as stat
import matplotlib
from numpy.linalg import inv
matplotlib.style.use('ggplot')
import scipy.fftpack

#%% Check
# Number of samplepoints
N = 1001
# sample spacing
T = 1000
x = np.linspace(0.0, N*T, N)
y = sinevec
yf = scipy.fftpack.fft(y)
xf = np.linspace(0.0, 1.0/(2.0*T), N/2)

fig, ax = plt.subplots()
ax.plot(xf, 2.0/N * np.abs(yf[:N/2]))
plt.xlim([0,0.00005])
plt.show()

#%% Exercise A
#Create delta function
def delta(t,t0):
    if t==t0:
        return 1
    if t!=t0:
        return 0
        
deltavec=[]
timevec=np.linspace(0, 600000,601)
for i in timevec:
    deltavec.append(delta(i,300000))

readvec=deltavec
freqvec=np.linspace(0,0.00005,51)

#%% Exercise B
#Create sine-wave function
sinevec=[]
timevec=np.linspace(0, 1000000,1001)
for i in timevec:
    sinevec.append(np.sin(i*2*np.pi/100000.))

readvec=sinevec
freqvec=np.linspace(0,0.00005,51)

#%% Exercise C
#Create saw tooth function
sawvec=[0]
timevec=np.linspace(0,1000000,1001)
for i in range(1,len(timevec)):
    if sawvec[i-1]<0.99:
        sawvec.append(sawvec[i-1]+1./100.)
    if sawvec[i-1]>=0.99:
        sawvec.append(0)

readvec=sawvec
freqvec=np.linspace(0,0.00005,51)

##Create saw tooth with 5 frequencies
#sinevec2=[]
#timevec=np.linspace(0, 1000000,1001)
#for i in timevec:
#    sinevec2.append(np.sin(i*2*np.pi/100000.)-0.5*np.sin(i*2*np.pi/100000.*2.)+0.25*np.sin(i*2*np.pi/100000.*3.)-0.125*np.sin(i*2*np.pi/100000.*4.))
#
#readvec=sinevec2
#freqvec=np.linspace(0,0.00005,51)


#%% Exercise D
#Create wavelength-varying saw tooth function
sawvec=[0]
timevec=np.linspace(0,1000000,1001)
wavelengthchooser=np.random.choice([-1,0,1])
period=100000.+wavelengthchooser*20000.
for i in range(1,len(timevec)):
    if sawvec[i-1]<1:
        sawvec.append(sawvec[i-1]+1./(1000./(1000000./period)))
    if sawvec[i-1]>=1:
        sawvec.append(0)
        wavelengthchooser=np.random.choice([-1,0,1])
        period=100000.+wavelengthchooser*20000.

readvec=sawvec
freqvec=np.linspace(0,0.00005,51)

#%% Exercise E
#Create wavelength-varying saw tooth function with noise
sawvec=[0]
timevec=np.linspace(0,1000000,1001)
wavelengthchooser=np.random.choice([-1,0,1])
period=100000.+wavelengthchooser*20000.
for i in range(1,len(timevec)):
    if sawvec[i-1]<1:
        sawvec.append(sawvec[i-1]+1./(1000./(1000000./period)))
    if sawvec[i-1]>=1:
        sawvec.append(0)
        wavelengthchooser=np.random.choice([-1,0,1])
        period=100000.+wavelengthchooser*20000.

for i in range(0,len(sawvec)):
    sawvec[i]=sawvec[i]+np.random.normal(0,0.5)

readvec=np.array(sawvec)
freqvec=np.linspace(0,0.00005,51)

#%% Exercise andere e
#Create wavelength-varying saw tooth function with noise
sawvec=[0]
timevec=np.linspace(0,1000000,1001)
wavelengthchooser=np.random.choice([-1,0,1])
period=100000.+wavelengthchooser*20000.
amplitude=1.+np.random.normal(0,0.1)
for i in range(1,len(timevec)):
    if sawvec[i-1]<amplitude:
        sawvec.append(sawvec[i-1]+amplitude/(1000./(1000000./period)))
    if sawvec[i-1]>=amplitude:
        sawvec.append(0)
        wavelengthchooser=np.random.choice([-1,0,1])
        period=100000.+wavelengthchooser*20000.
        amplitude=1.+np.random.normal(0,0.8)

readvec=np.array(sawvec)
freqvec=np.linspace(0,0.00005,51)
#%% All
#Make discrete fourier transform; t versie
def Fouriert(f,vector,tvec,dt):
    summation=[]
    for i in range(0,len(vector)-1):
        t=tvec[i]
        summation.append((vector[i])*np.exp(2.*np.pi*1j*f*t)*dt)
    SUM=np.sum(summation)/timevec[(len(timevec)-1)]
    return np.abs(SUM)**2.

#%%Make discrete fourier transform; k versie
def Fourier(f,vector,tvec,dt):
    summation=[]
    for i in range(0,len(vector)):
        summation.append((vector[i])*np.exp(-2.*np.pi*1j*f*i/len(vector)))
    SUM=np.sum(summation)#/np.sqrt(timevec[(len(timevec)-1)])
    return np.abs(SUM)**2
    
#Retrieve data fourier
Fouriervec=[]
for r in range(0,len(freqvec)):
    Fouriervec.append(Fourier(r,readvec,timevec,1001))

freqcheck=np.fft.fftfreq(len(readvec),d=1000)
fouriercheck=np.abs(np.fft.fft(readvec))**2

#Check
plt.figure(num=None, figsize=(7,3),dpi=150, facecolor='w', edgecolor='k')
plt.plot(timevec,readvec, 'r-',linewidth=3)
plt.ylabel('Amplitude',fontsize=15)
plt.xlabel('Time [yr]',fontsize=15)
plt.tick_params(axis='both', which='major', labelsize=15)

plt.figure(num=None, figsize=(7,3),dpi=150, facecolor='w', edgecolor='k')
plt.plot(freqvec[1:],Fouriervec[1:], 'r-',linewidth=3)
#plt.plot(freqcheck[:100],fouriercheck[:100], 'b-',linewidth=3)
plt.ylabel('Power',fontsize=15)
plt.xlabel(r'Frequency [yr$^{-1}$]',fontsize=15)
plt.xlim([0,0.00005])
plt.tick_params(axis='both', which='major', labelsize=15)

