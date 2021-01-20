"""
Bachelor Thesis Model Code
Iterative Definitions of Models
 - Kelvin-Voigt
 - Standard Linear Solid Model - Maxwell Representation
 - Standard Linear Solid Model - Kelvin-Voigt Representation
 
iterative_definitions.py
"""
import initial_conditions as init

m,k,eta,A,F_0 = init.parameters()

def kv(e,ev,ea,sig,dt):
    # Define iterative function for definining t+dt from point t according to kelvin-voigt model.
    signew = (k*e + eta*ev) if e>=0 else 0 # define force at t+dt from constitutive equation
    eanew = (A/m)*(F_0 - signew) # Define acceleration from force
    evnew = ev + dt*eanew # Define velocity from old velocity and acceleration
    enew = e + dt*evnew #Define strain from old strain and velocity
    return enew, evnew, eanew, signew
    

def SLSM_max(e,ev,ea,sig,sigv,dt):
    # Define iterative function for definining t+dt from point t according to SLSM-Maxwell model.
    k1,k2 = init.SLSM_max_k()
    sigvnew = (k2/eta)*(k1*e + ev*(eta*(k1+k2))/k2 - sig) if e>=0 else 0 # define force speed at t+dt from constitutive equation
    signew =  sig + dt*sigvnew if e>=0 else 0 # define force at t+dt from constitutive equation k1*e + ev*(eta*(k1+k2))/k2 - (eta/k2)*sigv
    eanew = (A/m)*(F_0 - signew) # Define acceleration from force
    evnew = ev + dt*eanew # Define velocity from old velocity and acceleration
    enew = e + dt*evnew #Define strain from old strain and velocity
    return enew, evnew, eanew, signew, sigvnew



def SLSM_kv(e,ev,ea,sig,sigv,dt):
    # Define iterative function for definining t+dt from point t according to SLSM-kelvin-voigt model.
    k1,k2 = init.SLSM_kv_k()
    sigvnew = (k1+k2/eta)*(e*k1*k2/(k1+k2) + ev*(eta*k1)/(k1+k2) - sig) if e>=0 else 0 # define force speed at t+dt from constitutive equation
    signew =  sig + dt*sigvnew if e>=0 else 0 # define force at t+dt from constitutive equation
    # signew = e*k1*k2/(k1+k2) + ev*k1*eta/(k1+k2) -  eta*sigv/(k1+k2) if e>=0 else 0
    # sigvnew = (k1+k2/eta)*(e*k1*k2/(k1+k2) + ev*(eta*k1)/(k1+k2) - sig)
    eanew = (A/m)*(F_0 - signew) # Define acceleration from force
    evnew = ev + dt*eanew # Define velocity from old velocity and acceleration
    enew = e + dt*evnew #Define strain from old strain and velocity
    return enew, evnew, eanew, signew, sigvnew
