"""
Bachelor Thesis Model Code
Sets of intial conditions

initial_conditions.py
"""

def parameters():
    m = 0.4 # mass (approx. mass of a boxing glove)
    k = 22000 # Single-spring constant (approx. for rubber foam)
    eta = 800# single-damper constant
    A = 0.01 # Surface
    F_0 = 800 # Constant force applied
    return m,k,eta,A,F_0

def SLSM_max_k():
    return 12000,20000

def SLSM_kv_k():
    return 60000,30000

def impact_kv(v0):
    return (0,v0,0,0)

def impact_SLSM(v0,eta):
    return (0,v0,0,0,v0*eta)

