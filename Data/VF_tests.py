"""
Variable Force Tests

VF_tests.py
"""
import numpy as np
import graphing as plot
import matplotlib.pyplot as plt
from pendulum import double_acc as da

m = 0.0015 # mass (approx. mass of a boxing glove)
E = 993000 # Single-spring constant (approx. for rubber foam)
eta = 150# single-damper constant
A = 0.0016 # Surface
F_0 = 1300 # Constant force applied



def kv_iter(e,ev,ea,sig,dt,t,F):
    # Define iterative function for definining t+dt from point t according to kelvin-voigt model.
    signew = (E*e + eta*ev) #if e>=0 else 0 # define force at t+dt from constitutive equation
    eanew = F(t) - (A/m)*signew # Define acceleration from force
    evnew = ev + dt*eanew # Define velocity from old velocity and acceleration
    enew = e + dt*evnew #Define strain from old strain and velocity
    return enew, evnew, eanew, signew



def kelvin_voigt(e_init,ev_init,ea_init,sig_init,dt,N,F):
    #Defines the full loop of kelvin voigt model, performing iteratve step N times, with step dt.
    (e,ev,ea,sig) = (e_init,ev_init,ea_init,sig_init)
    (elist,evlist,ealist,siglist) = ([e],[ev],[ea],[sig])
    for i in range(N):
        (enew,evnew,eanew,signew) = kv_iter(e,ev,ea,sig,dt,i,F)
        elist.append(enew)
        evlist.append(evnew)
        ealist.append(eanew)
        siglist.append(signew)
        (e,ev,ea,sig) = (enew,evnew,eanew,signew)
    return elist,evlist,ealist,siglist

def F_const(t):
    return F_0#0*t#F_0 *np.e**(-((t-10000)**2)/(5*10**7))

def F_gauss(t):
     return F_0 *np.e**(-((t-5000)**2)/(1*10**5))
 
def F_gauss_shift(t):
     return (2/5)*F_0 *np.e**(-((t-8000)**2)/(6*10**5))
 
def F_zero(t):
    return F_0 if t < 5 else 0

def F_square(t):
    return F_0 if 10000 < t < 20000 else 0
    
data = da('green_static_up')
real1,real2 = data[0]

e = 0
ev = 0
ea = 0
sig = 0
dt = 0.000001
N = 50000
FF = np.linspace(0,N*dt,N+1)
(el,evl,eal,sigl) = kelvin_voigt(e,ev,ea,sig,dt,N,F_gauss)
e = 0
ev = 0
ea = 0
sig = 0
#m = 0.025
(el2,evl2,eal2,sigl2) = kelvin_voigt(e,ev,ea,sig,dt,N,F_gauss_shift)
#ea1 = [-i for i in eal]
plt.figure(figsize=(12,8))
plt.plot(FF,[i/9.81 for i in eal2],label = 'Back')
plt.plot(FF,[i/9.81 for i in eal],label = 'Front')
plt.xlabel('Time (s)',fontsize=14)
plt.ylabel('Acceleration $(g)$',fontsize=14)
plt.legend()
plt.show()

plt.figure(figsize=(12,8))
plt.plot(real2[6215:6715,0]-0.6215,real2[6215:6715,1],label = 'Real')
plt.plot(FF,[i/9.81 for i in eal],label = 'Model')
plt.xlabel('Time (s)',fontsize=14)
plt.ylabel('Acceleration $(g)$',fontsize=14)
plt.legend()
plt.show()

plt.figure(figsize=(12,8))
plt.plot(real1[6215:6715,0]-0.6215,real1[6215:6715,1],label = 'Real')
plt.plot(FF,[i/9.81 for i in eal2],label = 'Model')
plt.xlabel('Time (s)',fontsize=14)
plt.ylabel('Acceleration $(g)$',fontsize=14)
plt.legend()
plt.show()


FF2 = np.linspace(0,N,N)
plt.figure(figsize=(12,8))
plt.plot(FF2*dt,[F_gauss(i) for i in FF2],label = 'Front')
plt.plot(FF2*dt,[F_gauss_shift(i) for i in FF2],label = 'Back')
plt.xlabel('Time (s)',fontsize=14)
plt.ylabel('Force $(N)$',fontsize=14)
plt.legend()
plt.show()
#E_tot = 4000*np.sqrt(5*10**7)

#for i in range(200,20200,200):
#    def F(t):
#        return i *np.e**(-((t-12000)**2)/((E_tot/i)**2))
#    (el,evl,eal,sigl) = kelvin_voigt(e,ev,ea,sig,dt,N)
#    fig=plt.figure(figsize=(12,8))
#    plt.subplot(211)
#    plt.plot(sigl)
#    plt.xlabel('Time (au)')
#    plt.ylabel('Force (au)')
#    plt.subplot(212)
#    plt.plot(F(FF))
#    plt.xlabel('Time (au)')
#    plt.ylabel('Force (au)')
#    #plt.savefig('force_shift/img'+str(i)+'.png')
#    plt.show()
#    #plt.close()