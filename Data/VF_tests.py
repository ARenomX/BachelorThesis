"""
Variable Force Tests

VF_tests.py
"""
import numpy as np
import graphing as plot

m = 0.4 # mass (approx. mass of a boxing glove)
k = 22000 # Single-spring constant (approx. for rubber foam)
eta = 600# single-damper constant
A = 0.01 # Surface
F_0 = 4000 # Constant force applied


def kv_iter(e,ev,ea,sig,dt,t):
    # Define iterative function for definining t+dt from point t according to kelvin-voigt model.
    signew = (k*e + eta*ev) #if e>=0 else 0 # define force at t+dt from constitutive equation
    eanew = (A/m)*(F(t) - signew) # Define acceleration from force
    evnew = ev + dt*eanew # Define velocity from old velocity and acceleration
    enew = e + dt*evnew #Define strain from old strain and velocity
    return enew, evnew, eanew, signew

def kelvin_voigt(e_init,ev_init,ea_init,sig_init,dt,N):
    #Defines the full loop of kelvin voigt model, performing iteratve step N times, with step dt.
    (e,ev,ea,sig) = (e_init,ev_init,ea_init,sig_init)
    (elist,evlist,ealist,siglist) = ([e],[ev],[ea],[sig])
    for i in range(N):
        (enew,evnew,eanew,signew) = kv_iter(e,ev,ea,sig,dt,i)
        elist.append(enew)
        evlist.append(evnew)
        ealist.append(eanew)
        siglist.append(signew)
        (e,ev,ea,sig) = (enew,evnew,eanew,signew)
    return elist,evlist,ealist,siglist

def F(t):
    return F_0 *np.e**(-((t-10000)**2)/(5*10**7))
    
e = 0
ev = 5
ea = 0
sig = F(0)
dt = 0.00001
N = 100000

(el,evl,eal,sigl) = kelvin_voigt(e,ev,ea,sig,dt,N)
plot.plot(sigl)
FF = np.linspace(0,100000,100000)
plot.plot_force(FF,F(FF))